#!/usr/bin/env python3
"""Bounded binary-derived Born versus exact-T diagnostic; no alloy-gap inputs.

Run with PYTHONPATH=src OPENBLAS_NUM_THREADS=1 .venv/bin/python tools/...
The output is not a physical self-consistent impurity prediction.
"""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from mct_research.impurity_tmatrix import branch_trace, t_derivative, t_matrix
from mct_research.sp3d5 import BinaryModel, host_embedding, star_embedding, star_potential


def encode(value):
    return {"real": float(np.real(value)), "imag": float(np.imag(value))}


def evaluate(v, embedded, states, energy, eta):
    z = energy + 1j * eta
    g = embedded.resolvent(z)
    gp = embedded.resolvent(z, derivative=1)
    t = t_matrix(v, g)
    tp = t_derivative(t, gp)
    born2 = v @ g @ v
    denominator = np.eye(len(v)) - v @ g
    imag_t = (t - t.conj().T) / (2j)
    optical_residual = t - t.conj().T - t.conj().T @ (g - g.conj().T) @ t
    out = {
        "energy_eV": energy, "eta_eV": eta,
        "denominator_min_singular": float(np.linalg.svd(denominator, compute_uv=False)[-1]),
        "causality_min_eigenvalue": float(np.linalg.eigvalsh(-imag_t)[0]),
        "optical_theorem_relative_residual": float(np.linalg.norm(optical_residual) / max(np.linalg.norm(t), 1)),
        "branches": {}
    }
    for name, a in states.items():
        u = t @ a
        local_norm = float(np.trace(a.conj().T @ a).real / a.shape[1])
        strength = float(np.trace(u.conj().T @ u).real / a.shape[1])
        # Positive norm at complex frequency is NOT -Re T'(z).
        cloud_modes = embedded.modes.conj().T @ u
        cloud_norm = float(np.sum(np.abs(cloud_modes / (z - embedded.energies)[:, None]) ** 2) / a.shape[1])
        tau = branch_trace(t, a)
        out["branches"][name] = {
            "first": encode(branch_trace(v, a)),
            "second": encode(branch_trace(born2, a)),
            "born_total": encode(branch_trace(v + born2, a)),
            "exact": encode(branch_trace(t, a)),
            "born_negative_derivative": encode(branch_trace(-v @ gp @ v, a)),
            "exact_negative_derivative": encode(branch_trace(-tp, a)),
            "incorrect_g_squared_negative_derivative": encode(branch_trace(t @ g @ g @ t, a)),
            "local_external_norm_squared": local_norm,
            "scattering_strength_eV_squared": strength,
            "full_host_cloud_norm": cloud_norm,
            "effective_detuning_eV": float(np.sqrt(strength / cloud_norm)),
            "local_scattering_overlap": encode(tau / np.sqrt(local_norm * strength)),
        }
    if eta == 0:
        out["off_continuum_min_negative_Tprime_eigenvalue"] = float(np.linalg.eigvalsh(-tp)[0])
    return out


def run(args):
    if any(eta <= 0 for eta in args.eta):
        raise ValueError("The retarded broadening list must be positive; real CdTe gap control is added separately")
    path = Path("data/materials/schindler2012_sp3d5.json")
    parameters = json.loads(path.read_text())
    raw = {name: BinaryModel(parameters[name]) for name in ("HgTe", "CdTe")}
    # Align the actual reconstructed Gamma8 energies, then impose the SOURCE offset.
    models = {name: BinaryModel(parameters[name], -raw[name].gamma_sectors()["E8"]
                               - (args.offset if name == "CdTe" else 0)) for name in raw}
    output = {
        "claim_status": "CALCULATED: binary-derived finite-q diagnostic, not physical self-consistent impurity",
        "empirical_alloy_gap_inputs": [],
        "parameter_file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "source": parameters["source"],
        "offset_eV": args.offset,
        "te_share": args.te_share,
        "quadrature": "even midpoint primitive reciprocal parallelepiped grid; no Gamma point",
        "binary": {}, "rows": []
    }
    for name, model in models.items():
        sec = model.gamma_sectors()
        output["binary"][name] = {"E6_eV": sec["E6"], "E8_eV": sec["E8"], "gap_eV": sec["E6"] - sec["E8"]}
    for host, guest in (("HgTe", "CdTe"), ("CdTe", "HgTe")):
        sec = models[host].gamma_sectors()
        states = {"6": star_embedding(np.zeros(3)) @ sec["states6"],
                  "8": star_embedding(np.zeros(3)) @ sec["states8"]}
        v = star_potential(models[host], models[guest], args.te_share)
        for mesh in args.mesh:
            if mesh % 2 or mesh < 2:
                raise ValueError("Use even grids >=2 to avoid a discrete Gamma pole")
            embedded = host_embedding(models[host], mesh)
            normalization_error = np.linalg.norm(embedded.modes @ embedded.modes.conj().T - np.eye(90))
            print(f"{guest} in {host}: mesh={mesh}, completeness error={normalization_error:.3g}", flush=True)
            for eta in args.eta:
                for label, energy in (("Gamma6_pole", sec["E6"]), ("Gamma8_pole", sec["E8"]),
                                      ("common_mode", (sec["E6"] + sec["E8"]) / 2)):
                    row = evaluate(v, embedded, states, energy, eta)
                    row.update(host=host, guest=guest, mesh=mesh, reference=label, completeness_error=normalization_error)
                    output["rows"].append(row)
                    if label == "common_mode":
                        b = row["branches"]
                        print(f"  eta={eta:g}: common Born2 mass={(b['6']['second']['real']-b['8']['second']['real'])/2:.6g}, "
                              f"exact full mass={(b['6']['exact']['real']-b['8']['exact']['real'])/2:.6g}", flush=True)
            if host == "CdTe":
                energy = (sec["E6"] + sec["E8"]) / 2
                row = evaluate(v, embedded, states, energy, 0)
                row.update(host=host, guest=guest, mesh=mesh, reference="common_mode_gap_real", completeness_error=normalization_error)
                output["rows"].append(row)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mesh", type=int, nargs="+", default=[6, 10, 14])
    parser.add_argument("--eta", type=float, nargs="+", default=[0.05, 0.02])
    parser.add_argument("--offset", type=float, default=0.4)
    parser.add_argument("--te-share", type=float, default=0.25)
    parser.add_argument("--output", type=Path, default=Path("data/calculated/sp3d5_impurity_diagnostic.json"))
    run(parser.parse_args())
