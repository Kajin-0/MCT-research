"""Fixed algebraic pilot budget and small causal aliasing witness, not DFT."""
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("r07_ref_bounds", HERE/"evaluate_reference_bound.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
I = ref.I


def ring_host(size):
    h = np.zeros((size, size))
    for i in range(size):
        h[i, (i+1)%size] -= 1
        h[(i+1)%size, i] -= 1
    return h


def periodic_profile(size, strengths, positions):
    diagonal = np.zeros(size)
    for strength, position in zip(strengths, positions):
        diagonal[position % size] += strength
    return np.diag(diagonal)


def aliasing_witness():
    rows = []
    # One fixed small witness, not a parameter/composition scan.
    z = 3+.1j
    for n in (4, 12):
        h0 = ring_host(n)
        first = periodic_profile(n, [.1], [0])
        second = periodic_profile(n, [.13, -.03], [0, 4])
        phi = np.ones(n)/np.sqrt(n)
        a = z+2  # Exact host Gamma eigenvalue -2.
        r = [phi@np.linalg.solve(z*np.eye(n)-h0-v, phi) for v in (first, second)]
        k = [a-1/value for value in r]
        rows.append({"ring_size": n, "potential_difference_norm_eV": float(np.linalg.norm(first-second, 2)),
                     "projected_resolvent_difference_eV_inverse": float(abs(r[0]-r[1])),
                     "scaled_reaction_kernel_difference_eV": float(n*abs(k[0]-k[1])),
                     "spectral_data_scope": "exact synthetic finite ring only"})
    return rows


def evaluate():
    w, eta, p, branch_budget, tail_budget = I("0.5"), I("0.025"), I("0.05"), I("0.001"), I("0.0005")
    moment_max = 16*w/(25*ref.sqrt_enclosure(I(5)))
    allowed_sigma = tail_budget*p/(w+moment_max)
    norm_sensitivity = (I(7)/5*w**2)/(ref.arith.PI*eta**2*p)
    allowed_operator_error = tail_budget/norm_sensitivity
    return {"claim_status": "CALCULATED conditional design arithmetic; no physical error certified",
            "window_half_width_eV": "0.5", "eta_eV": "0.025", "mass_floor": "0.05",
            "total_numerical_ordering_budget_eV": (2*branch_budget).record(),
            "per_sector_budget_eV": branch_budget.record(), "per_sector_tail_allocation_eV": tail_budget.record(),
            "max_omitted_weight_for_tail_allocation": allowed_sigma.record(),
            "unstructured_operator_norm_sensitivity_dimensionless": norm_sensitivity.record(),
            "unstructured_operator_error_for_half_sector_budget_eV": allowed_operator_error.record(),
            "operator_precision_requirement_accepted": False,
            "all_material_error_bounds": None,
            "aliasing_witness": aliasing_witness(),
            "driver_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "prior_evaluator_sha256": hashlib.sha256((HERE/"evaluate_reference_bound.py").read_bytes()).hexdigest(),
            "DFT_launched": False, "physical_xc": None}


if __name__ == "__main__":
    path = HERE/"acquisition_budget.json"
    if path.exists():
        raise FileExistsError("never overwrite a research result")
    result = evaluate()
    path.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in ("max_omitted_weight_for_tail_allocation", "unstructured_operator_error_for_half_sector_budget_eV", "aliasing_witness")}, indent=2))
