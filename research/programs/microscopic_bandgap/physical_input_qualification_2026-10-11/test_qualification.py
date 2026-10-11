"""Focused existing-source and synthetic proof checks; no native jobs."""
import hashlib
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def audit():
    return json.loads((HERE / "existing_audit.json").read_text())


def test_native_physical_projection_audit_scope():
    a = audit()
    assert a["native_reference_SCF_gates"] == [True, True]
    assert a["native_source_phi_gram_error"] < 1e-12
    assert a["native_Gamma_kernel_norm_recomputed_eV"] < 5e-6
    assert not a["supervisor_records_opened"] and not a["native_jobs_launched"]
    assert not a["material_uncertainty_certified"] and a["physical_xc"] is None
    assert len(a["verified_sources_sha256"]) == 29
    assert not any(path.endswith("/state.json") for path in a["verified_sources_sha256"])


def test_native_sector_weights_and_reference_leakage():
    a = audit()
    for name, d in [("Gamma6", 2), ("Gamma8", 4)]:
        sector = a["sectors"][name]
        weights = np.array(sector["resolved_weights_without_prefix_renormalization"])
        assert len(weights) == 44 and np.all(weights >= 0)
        assert abs(weights.sum()-1) < 1e-10
        assert len(sector["native_singular_values"]) == d
        assert min(sector["native_singular_values"]) > 1-3e-12
        assert sector["maximum_matched_edge_displacement_eV"] < 5e-6
        assert len(sector["source_edge_energies_eV"]) == d
    assert a["prepared_pair"]["periodic_Cd_fraction"] == 1/8
    assert all(not v["accepted_scf"] for v in a["prepared_pair"]["SCF_members"].values())
    assert not a["existing_interior_SQS"]["Gamma_projected_spectral_contractions_present"]


def test_saved_completed_source_provenance():
    a = audit()
    for path, expected in a["verified_sources_sha256"].items():
        p = Path(path)
        if not p.is_absolute():
            p = HERE.parents[3] / p
        h = hashlib.sha256()
        with p.open("rb") as f:
            for chunk in iter(lambda: f.read(262144), b""):
                h.update(chunk)
        assert h.hexdigest() == expected, path
    assert hashlib.sha256((HERE/"audit_existing.py").read_bytes()).hexdigest() == a["driver_sha256"]
