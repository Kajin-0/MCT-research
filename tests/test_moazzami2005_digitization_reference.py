import json
from pathlib import Path

from tools.audit_moazzami2005_digitization_sensitivity import audit

ROOT = Path(__file__).resolve().parents[1]


def test_digitization_sensitivity_reference() -> None:
    expected = json.loads(
        (ROOT / "validation/moazzami2005_digitization_sensitivity_reference_result.json").read_text(
            encoding="utf-8"
        )
    )
    assert audit(ROOT) == expected
