"""Read-only native Gamma audit. Writes only into this MCT research package.

Use the already installed DFT Python environment for h5py. No QE drivers,
supervisor records, MPI, process inspection or DFT-repository writes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from xml.etree import ElementTree as ET

import numpy as np

HERE = Path(__file__).resolve().parent
MCT = HERE.parents[3]
DFT = Path("/home/User/opencode_workspace/DFT")
REVIEW_PATH = MCT / "data/calculated/r07_completed_reference_review_20261011.json"
REVIEW = json.loads(REVIEW_PATH.read_text())
RUNS = [DFT / r["run"] for r in REVIEW["native_terminal_evidence"]]
sys.dont_write_bytecode = True
sys.path.insert(0, str(DFT / "src"))
from mct_dft.qe_wavefunctions import read_spinors, cross_spinor_overlap  # noqa: E402


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(262144), b""):
            h.update(chunk)
    return h.hexdigest()


def native_gamma(run):
    save = run / "out/r07_open.save"
    schema = save / "data-file-schema.xml"
    tree = ET.parse(schema)
    found = [(i, row) for i, row in enumerate(tree.findall(".//ks_energies"))
             if np.linalg.norm(np.fromstring(row.findtext("k_point"), sep=" ")) < 1e-10]
    if len(found) != 1:
        raise ValueError("require exactly one explicit native Gamma")
    index, row = found[0]
    energies = np.fromstring(row.findtext("eigenvalues"), sep=" ") * 27.211386245988
    source = save / f"wfc{index+1}.hdf5"
    c, g, k = read_spinors(source)
    if len(c) != len(energies) or len(c) != 44:
        raise ValueError("fixed accepted 44-band native dataset required")
    return tree, energies, c, g, k


def main(output):
    output = Path(output).resolve()
    if output.parent != HERE or output.exists():
        raise ValueError("fresh output in this MCT package only")
    verified = {str(REVIEW_PATH.relative_to(MCT)): digest(REVIEW_PATH)}
    # Skip the two historical supervisor state paths entirely, even for hashing.
    for rel, expected in REVIEW["external_sources_sha256"].items():
        if rel.endswith("/state.json"):
            continue
        actual = digest(DFT / rel)
        if actual != expected:
            raise ValueError(f"pinned completed source changed: {rel}")
        verified[str(DFT / rel)] = actual
    module = DFT / "src/mct_dft/qe_wavefunctions.py"
    verified[str(module)] = digest(module)
    records = [json.loads((run / "result.json").read_text()) for run in RUNS]
    assignments = [json.loads((run / "gamma/signed_gap.json").read_text()) for run in RUNS]
    for record in records:
        if not all(record[k] for k in ("accepted_scf", "job_done", "exx_converged")) or record["returncode"] != 0:
            raise ValueError("unaccepted native reference")
    data = [native_gamma(run) for run in RUNS]
    for query in ("./output/atomic_structure/cell", "./output/atomic_structure/atomic_positions"):
        nodes = [d[0].find(query) for d in data]
        if len(nodes[0]) != len(nodes[1]):
            raise ValueError("physical frames differ")
        for a, b in zip(*nodes):
            if a.attrib.get("name") != b.attrib.get("name"):
                raise ValueError("species/order differ")
            np.testing.assert_allclose(np.fromstring(a.text, sep=" "), np.fromstring(b.text, sep=" "), atol=1e-12, rtol=0)
    selections = []
    for assignment in assignments:
        selections.append([i for name in ("Gamma6", "Gamma8")
                           for i in range(assignment[name+"_bands_1based"][0]-1,
                                          assignment[name+"_bands_1based"][1])])
    _, e0, c0, g0, k0 = data[0]
    _, e1, c1, g1, k1 = data[1]
    phi = c0[selections[0]]
    overlap = cross_spinor_overlap(c1, g1, k1, phi, g0, k0)
    flat = phi.reshape(6, -1)
    gram_error = float(np.linalg.norm(flat.conj() @ flat.T - np.eye(6), 2))
    report_rel = next(r for r in REVIEW["external_sources_sha256"] if "/fock_operator_control_" in r)
    report = json.loads((DFT / report_rel).read_text())
    sectors = {}
    for label, cols, idx in [("Gamma6", slice(0, 2), selections[1][:2]),
                             ("Gamma8", slice(2, 6), selections[1][2:])]:
        singular = np.linalg.svd(overlap[idx, cols], compute_uv=False)
        np.testing.assert_allclose(singular, report["sector_overlap_singular_values"][label], atol=3e-15, rtol=0)
        weights = np.sum(np.abs(overlap[:, cols])**2, axis=1)/(cols.stop-cols.start)
        original = e0[selections[0][cols]]
        target = e1[idx]
        sectors[label] = {
            "source_edge_energies_eV": original.tolist(),
            "comparison_edge_energies_eV": target.tolist(),
            "source_edge_center_eV": float(original.mean()),
            "comparison_edge_center_eV": float(target.mean()),
            "maximum_matched_edge_displacement_eV": float(np.max(np.abs(original[:, None]-target))),
            "native_singular_values": singular.tolist(),
            "reported_leakage_upper_exact_eigenpair_assumption": float(1-singular.min()**2),
            "resolved_weights_without_prefix_renormalization": weights.tolist(),
            "resolved_weight_sum": float(weights.sum()),
        }
    h0 = e0[selections[0]]
    z = complex(report["z_eV"]["real"], report["z_eV"]["imag"])
    r = overlap.conj().T @ (overlap/(z-e1[:, None]))
    k = np.diag(z-h0)-np.linalg.inv(r)
    np.testing.assert_allclose(np.linalg.norm(k, 2), report["Gamma_reaction_kernel_norm_eV"], rtol=0, atol=5e-15)
    pair = DFT / "calculations/r07/cd_in_hg_pair_n2_k2_q2_e90_f120_prepare"
    prepared = json.loads((pair / "preparation.json").read_text())
    dry = {}
    for member in ("host", "impurity"):
        path = pair / member / "pw_dry_result.json"
        record = json.loads(path.read_text())
        if not record["accepted_native_dry_run"] or record["accepted_scf"]:
            raise ValueError("existing capability record changed scope")
        input_path = pair / member / "pw.in"
        if digest(input_path) != prepared["inputs_sha256"][member]["pw.in"]:
            raise ValueError("prepared input changed")
        verified[str(path)], verified[str(input_path)] = digest(path), digest(input_path)
        dry[member] = {"accepted_scf": False, "estimated_RAM_GiB": record["estimated_total_dynamical_RAM_QE_GB"],
                       "full_SCF_peak_memory_measured": record["full_SCF_peak_memory_measured"],
                       "dry_seconds": record["wall_seconds"],
                       "accepted_member_SCF_result_present": (pair/member/"result.json").exists()}
    verified[str(pair / "preparation.json")] = digest(pair / "preparation.json")
    sqs = DFT / "results/tables/hgcdte_x020_scf_edges.json"
    raw_sqs = json.loads(sqs.read_text())
    # Do not copy or use the empirical benchmarks in this mixed-provenance file.
    soc_row = next(row for row in raw_sqs["runs"] if row["soc"])
    verified[str(sqs)] = digest(sqs)
    result = {
        "claim_status": "CALCULATED existing-data native numerical reference audit; material/impurity inputs remain unqualified",
        "base_commit": "b19fc65", "driver_sha256": digest(Path(__file__)),
        "verified_sources_sha256": verified, "supervisor_records_opened": False,
        "native_reference_runs": [str(run) for run in RUNS], "native_reference_SCF_gates": [True, True],
        "native_source_phi_gram_error": gram_error,
        "native_Gamma_kernel_norm_recomputed_eV": float(np.linalg.norm(k, 2)),
        "comparison_Gamma_energies_eV": e1.tolist(), "sectors": sectors,
        "prepared_pair": {"periodic_Cd_fraction": prepared["periodic_substitute_fraction"], "n_atoms": prepared["n_atoms"],
                           "SCF_members": dry, "status": "capability only; no accepted impurity operator"},
        "existing_interior_SQS": {"soc": True, "source_run_label": soc_row["run"], "edge_by_band_count_eV": soc_row["band_edges"]["gap_eV"],
                                  "Gamma_projected_spectral_contractions_present": False,
                                  "HSE_impurity_or_random_alloy_error_budget_present": False,
                                  "interpretation": "PBE band-count edge; cannot qualify retained physical Gamma ordering"},
        "physical_xc": None, "native_jobs_launched": False,
        "material_uncertainty_certified": False,
        "limits": ["Exact-source spectral bounds below require native eigenpair/metric assumptions; gram/SCF tolerances do not certify a true HSE operator residual",
                   "Gamma f360-f120 numerical comparison cannot bound all finite-q impurity exchange errors",
                   "A finite periodic substituted cell and a Bernoulli thermodynamic alloy have different observables/laws"],
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"sources_verified": len(verified), "kernel_eV": result["native_Gamma_kernel_norm_recomputed_eV"],
                      "source_phi_gram_error": gram_error, "physical_xc": None,
                      "impurity_status": result["prepared_pair"]["status"]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    main(parser.parse_args().output)
