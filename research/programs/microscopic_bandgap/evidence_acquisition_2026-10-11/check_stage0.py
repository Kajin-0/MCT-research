"""Read-only Stage-0 provenance and qualification checks; no spectral fit."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[3]


def main():
    ledger = json.loads((PACKAGE / "stage0_sources.json").read_text())
    assert ledger["decision"] == "STAGE0_NO_GO_RAW_AND_ASSAY_PACKAGE_NOT_ACCESSIBLE"
    assert ledger["stage1_admitted"] is False
    assert ledger["physical_xc"] is None
    assert ledger["new_operational_sign_bracket"] is None
    assert ledger["accepted_raw_bundles"] == 0
    # These check declared scope; they do not independently observe processes.
    assert all(value == 0 for value in ledger["controls"].values())
    records = ledger["local_inputs"]
    assert len({r["path"] for r in records}) == len(records)
    for record in records:
        path = ROOT / record["path"]
        raw = path.read_bytes()
        assert len(raw) == record["bytes"], path
        assert hashlib.sha256(raw).hexdigest() == record["sha256"], path
    sources = {s["id"]: s for s in ledger["sources"]}
    assert len(sources) == len(ledger["sources"])
    assert all(s["url"].startswith("https://") for s in sources.values())
    assert all(s["raw_bundle_located"] is False for s in sources.values())
    for sample in ledger["samples"]:
        assert sample["source_id"] in sources
        assert sample["accepted"] is False
        assert sample["independent_sample_composition_interval"] is None
        assert sample["complete_uncertainty_budget"] is False
        assert sample["accessible_calibrated_raw_bundle"] is False
    assert ledger["next_action"]["status"] == "one_unsent_request_only"
    assert ledger["next_action"]["current_custodian_verified"] is False
    assert ledger["domain_D"]["status"] == "OPEN_not_certified"

    links = 0
    for path in PACKAGE.glob("stage0_*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if target.startswith(("https://", "http://", "#")):
                continue
            assert (path.parent / target.split("#", 1)[0]).resolve().is_file(), target
            links += 1

    # Exact pilot arithmetic, with no uncertainty distribution invented.
    left, right = Fraction(3, 20), Fraction(37, 200)
    half_width = Fraction(1, 500)
    midpoint = Fraction(67, 400)
    assert midpoint == (left + right) / 2
    assert (left - half_width, right + half_width) == (
        Fraction(37, 250), Fraction(187, 1000)
    )
    assert right + half_width - left + half_width == Fraction(39, 1000)
    for nominal in (Fraction(7, 40), Fraction(31, 200)):
        assert all(abs(nominal - target) > half_width for target in (left, right))
    # This excludes printed nominal values only, not unmeasured true fractions.

    print(json.dumps({
        "decision": ledger["decision"],
        "pinned_local_inputs_verified": len(records),
        "source_access_rows_checked": len(sources),
        "unaccepted_sample_rows_checked": len(ledger["samples"]),
        "stage0_local_links_verified": links,
        "pilot_arithmetic": "exact design check; no accepted assays",
        "physical_certificate": "none asserted",
    }, indent=2))


if __name__ == "__main__":
    main()
