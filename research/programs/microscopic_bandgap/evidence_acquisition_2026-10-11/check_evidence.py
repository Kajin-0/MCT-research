"""Read-only provenance and exact symbolic checks; no material calculation."""

from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import re
import sys


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[3]


def check_provenance():
    inventory = json.loads((PACKAGE / "local_evidence_inventory.json").read_text())
    records = inventory["records"]
    assert len(records) == inventory["record_count"]
    assert len({r["path"] for r in records}) == len(records)
    for r in records:
        p = ROOT / r["path"]
        assert p.is_file(), p
        raw = p.read_bytes()
        assert len(raw) == r["bytes"], p
        assert sha256(raw).hexdigest() == r["sha256"], p
    actual = {p.relative_to(ROOT).as_posix()
              for p in (ROOT / "data/calculated").glob("*.json")}
    inventoried = {r["path"] for r in records
                  if r["path"].startswith("data/calculated/")
                  and r["path"].endswith(".json")}
    assert actual == inventoried and len(actual) == 22
    ledger = json.loads((PACKAGE / "sources.json").read_text())
    sources = ledger["sources"]
    assert len(sources) == ledger["source_count"] == 24
    assert len({s["id"] for s in sources}) == len(sources)
    assert len({s["doi"] for s in sources}) == len(sources)
    assert ledger["physical_xc"] is None
    assert ledger["physical_uniform_branch_residual_eV"] is None
    assert ledger["physical_lower_composition_modulus_eV_per_x"] is None
    paths = {r["path"] for r in records}
    matrix = (PACKAGE / "source_evidence_matrix.md").read_text()
    fresh_checked = 0
    for s in sources:
        assert re.fullmatch(r"10\.\d{4,9}/\S+", s["doi"]), s["id"]
        assert s["doi_url"] == "https://doi.org/" + s["doi"]
        assert s["primary_url"].startswith("https://")
        assert s["doi"] in matrix and s["matrix_id"] in matrix
        assert s["certified_physical_gates"] == []
        for name in s["local_audits"]:
            assert name in paths and (ROOT / name).is_file(), (s["id"], name)
        if s["pdf_sha256"]:
            assert re.fullmatch(r"[0-9a-f]{64}", s["pdf_sha256"])
        if s["hash_provenance"] == "inherited_primary_audit_not_rehashed":
            assert any(s["pdf_sha256"] in (ROOT / p).read_text()
                       for p in s["local_audits"]), s["id"]
        if "--verify-temporary-copies" in sys.argv and s["temporary_copy"]:
            assert sha256(Path(s["temporary_copy"]).read_bytes()).hexdigest() == s["pdf_sha256"]
            fresh_checked += 1
    return len(records), len(sources), fresh_checked


def check_local_links():
    count = 0
    for p in PACKAGE.glob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", p.read_text()):
            if target.startswith(("https://", "http://")):
                continue
            destination = target.split("#", 1)[0]
            if destination:
                assert (p.parent / destination).resolve().is_file(), (p.name, target)
                count += 1
    return count


def check_exact_information_and_design_bounds():
    # Three exact observations and positive sampled secants do not bound
    # the all-pairs derivative. This is a counterexample, never a material law.
    lo, mid, hi = F(3, 20), F(67, 400), F(37, 200)
    assert mid == (lo + hi) / 2
    def null_polynomial(x):
        return (x - lo) * (x - mid) * (x - hi)
    assert all(null_polynomial(x) == 0 for x in (lo, mid, hi))
    derivative_at_mid = (mid - lo) * (mid - hi)
    assert derivative_at_mid == -F(49, 160000)
    witness_amplitude = -2 / derivative_at_mid
    assert 1 + witness_amplitude * derivative_at_mid == -1
    def witnessed_mass(x):
        return x + witness_amplitude * null_polynomial(x)
    assert all(witnessed_mass(x) == x for x in (lo, mid, hi))
    assert all((witnessed_mass(b)-witnessed_mass(a))/(b-a) == 1
               for a, b in ((lo, mid), (mid, hi)))

    # Independent exact finite-bath subtraction verifies the secant identity
    # on a support-free interval; it supplies no physical measure.
    e1, e2 = F(1, 10), F(3, 20)
    t = (F(1, 2), F(1))
    sector_weights = ((F(1, 50), F(3, 100)), (F(1, 100), F(1, 25)))
    bs = []
    for weights in sector_weights:
        def kernel(e):
            return sum(w / (e - ti) for w, ti in zip(weights, t))
        b = (kernel(e1) - kernel(e2)) / (e2 - e1)
        assert b == sum(w / ((e1-ti)*(e2-ti)) for w, ti in zip(weights, t))
        assert b >= 0
        bs.append(b)
    b6, b8 = bs
    ratio = (b8 - b6) / (2 + b6 + b8)
    assert abs(ratio) < 1
    assert (1-ratio)/2 >= 0 and (1+ratio)/2 >= 0
    assert (1-ratio)/2 + (1+ratio)/2 == 1

    dx = F(1, 500)
    assert (hi+dx)-(lo-dx) == F(39, 1000)
    assert (mid+dx)-(lo-dx) == (hi+dx)-(mid-dx) == F(43, 2000)
    assert 2 * F(5, 1000) == F(10, 1000)
    assert 300 + 2 * 1800 == 3900
    assert F(3900, 3600) <= F(10834, 10000)
    assert 200 * 2 * 3 == 1200
    assert 31 * 10000 * 8 == 2480000
    assert 64 * 64 * 16 == 65536


def main():
    records, sources, fresh = check_provenance()
    links = check_local_links()
    check_exact_information_and_design_bounds()
    print(json.dumps({"decision": "MISSING_QUALIFIED_PHYSICAL_EVIDENCE_STOP",
                      "frozen_records_verified": records,
                      "primary_publications": sources,
                      "fresh_pdf_hashes_verified": fresh,
                      "local_links_verified": links,
                      "exact_symbolic_checks": "passed_nonmaterial_witnesses_only",
                      "new_native_calculations": 0}, indent=2))


if __name__ == "__main__":
    main()
