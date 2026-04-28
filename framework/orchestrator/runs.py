"""Run-id generation, sidecar metadata, and SQLite checkpointer helpers.

A "run" is one invocation of the generation pipeline. Each run is given a
unique ``run_id`` that doubles as the LangGraph ``thread_id`` for its
checkpoint, and is the key the user passes to ``--resume`` to continue an
interrupted run from the last completed node.

Layout under ``outputs/.checkpoints/``:
    autospectest.sqlite       single shared LangGraph checkpoint DB
    <run_id>.json             per-run metadata sidecar (input path, model, ...)
"""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


CHECKPOINT_DIR = Path("outputs") / ".checkpoints"
CHECKPOINT_DB = CHECKPOINT_DIR / "autospectest.sqlite"


@dataclass
class RunMetadata:
    """Sidecar metadata describing a generation run."""

    run_id: str
    input_path: str
    model: str
    output_dir: str
    started_at: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "RunMetadata":
        return cls(
            run_id=data["run_id"],
            input_path=data["input_path"],
            model=data["model"],
            output_dir=data["output_dir"],
            started_at=data["started_at"],
        )


def _slugify(value: str) -> str:
    """Reduce a project name to a filesystem-safe slug."""
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug or "run"


def make_run_id(project_name: str) -> str:
    """Build a sortable, collision-resistant run id."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    suffix = uuid.uuid4().hex[:6]
    return f"{_slugify(project_name)}-{timestamp}-{suffix}"


def sidecar_path(run_id: str) -> Path:
    return CHECKPOINT_DIR / f"{run_id}.json"


def write_sidecar(metadata: RunMetadata) -> Path:
    """Persist run metadata next to the checkpoint DB."""
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    path = sidecar_path(metadata.run_id)
    path.write_text(metadata.to_json(), encoding="utf-8")
    return path


def read_sidecar(run_id: str) -> RunMetadata:
    """Load a previously-written sidecar. Raises FileNotFoundError if missing."""
    path = sidecar_path(run_id)
    if not path.exists():
        raise FileNotFoundError(
            f"No sidecar found for run_id '{run_id}' at {path}. "
            "Either the run id is wrong or the sidecar was deleted."
        )
    return RunMetadata.from_dict(json.loads(path.read_text(encoding="utf-8")))


def make_run_metadata(
    *,
    run_id: str,
    input_path: str,
    model: str,
    output_dir: str,
) -> RunMetadata:
    return RunMetadata(
        run_id=run_id,
        input_path=str(input_path),
        model=model,
        output_dir=str(output_dir),
        started_at=datetime.now(timezone.utc).isoformat(),
    )


