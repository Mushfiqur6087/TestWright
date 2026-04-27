"""Export verification suite data to JSON format."""

import json

from testwright.models.schemas import VerificationSuiteOutput


def export_verification_json(output: VerificationSuiteOutput, file_path: str) -> str:
    """Write a VerificationSuiteOutput to a JSON file. Returns the file path."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(output.to_dict(), f, indent=2, ensure_ascii=False)
    return file_path
