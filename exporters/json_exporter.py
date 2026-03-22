"""Export test suite data to JSON format."""

import json

from testwright.models.schemas import TestSuiteOutput


def export_json(output: TestSuiteOutput, file_path: str) -> str:
    """Export final output to JSON file.

    Args:
        output: The test suite output to export.
        file_path: Path to write the JSON file.

    Returns:
        The file path that was written to.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(output.to_dict(), f, indent=2, ensure_ascii=False)
    return file_path
