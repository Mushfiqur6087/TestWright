"""Verification pipeline orchestrator.

Runs the standalone verify step: loads an already-generated test-cases.json,
filters to positive tests, fans the VerificationPlannerAgent out across them
in parallel, and writes verifications.json.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from autospectest.framework.agents.base import BaseAgent
from autospectest.framework.verification.planner import (
    VerificationPlannerAgent,
    compute_coverage_summary,
)
from autospectest.exporters.verification_json_exporter import export_verification_json
from autospectest.framework.schemas.schemas import TestSuiteOutput, VerificationSuiteOutput


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run_verification(
    test_cases_json_path: str,
    spec_path: str,
    api_key: str,
    model: str = "gpt-4o",
    provider: str = "openai",
    output_path: Optional[str] = None,
    cross_role_spec_paths: Optional[List[str]] = None,
    max_workers: int = 8,
    debug: bool = False,
    debug_file: str = "debug_log.txt",
) -> str:
    """Execute the verification pipeline. Returns the output file path."""

    input_path = Path(test_cases_json_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Test cases JSON not found: {input_path}")

    main_spec = Path(spec_path)
    if not main_spec.exists():
        raise FileNotFoundError(f"Functional spec not found: {main_spec}")

    peer_paths: List[Path] = []
    for p in cross_role_spec_paths or []:
        pp = Path(p)
        if not pp.exists():
            raise FileNotFoundError(f"Cross-role spec not found: {pp}")
        peer_paths.append(pp)

    out_path = Path(output_path) if output_path else input_path.with_name("verifications.json")

    print(f"  Input test cases: {input_path}")
    print(f"  Main spec: {main_spec}")
    if peer_paths:
        print(f"  Cross-role specs: {[str(p) for p in peer_paths]}")
    print(f"  Output: {out_path}")

    with open(input_path, "r", encoding="utf-8") as f:
        test_cases_data = json.load(f)
    suite = TestSuiteOutput.from_dict(test_cases_data)

    spec_text = _read_text(main_spec)
    peer_specs = [_read_text(p) for p in peer_paths]

    positive_cases = [tc for tc in suite.test_cases if tc.test_type == "positive"]
    total_cases = len(suite.test_cases)
    print(f"  Test cases loaded: {total_cases} total, "
          f"{len(positive_cases)} positive (verification candidates)")

    if debug:
        BaseAgent.reset_debug_state()
        BaseAgent.init_debug_session(debug_file=debug_file, model=model)

    agent = VerificationPlannerAgent(
        api_key=api_key,
        model=model,
        provider=provider,
        debug=debug,
        debug_file=debug_file,
    )

    t0 = time.time()
    records = agent.run(
        test_cases=positive_cases,
        spec_text=spec_text,
        peer_specs=peer_specs,
        nav_graph=suite.navigation_graph,
        max_workers=max_workers,
    )
    elapsed = time.time() - t0

    coverage_summary = compute_coverage_summary(records)

    output = VerificationSuiteOutput(
        project_name=suite.project_name,
        base_url=suite.base_url,
        generated_at=datetime.now().isoformat(),
        source_test_cases_file=str(input_path),
        source_spec_files=[str(main_spec)] + [str(p) for p in peer_paths],
        verifications=records,
        coverage_summary=coverage_summary,
    )

    export_verification_json(output, str(out_path))

    print(f"\nVerification complete in {elapsed:.1f}s")
    print(f"  Records emitted: {coverage_summary['total_records']}")
    print(f"    verifiable:    {coverage_summary['verifiable']}")
    print(f"    manual_only:   {coverage_summary['manual_only']}")
    print(f"    not_coverable: {coverage_summary['not_coverable']}")
    print(f"  By type: {coverage_summary['by_type']}")
    print(f"  Output: {out_path}")

    return str(out_path)
