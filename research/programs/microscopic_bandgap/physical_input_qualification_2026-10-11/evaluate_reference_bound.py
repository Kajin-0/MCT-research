"""U1-U3 conditional bounds from existing data, with outward arithmetic.

No native dataset is evaluated, no spectrum/grid is scanned. These are
rounded-input conditional reference controls, not physical material error bars.
"""
from decimal import Decimal, ROUND_HALF_EVEN, localcontext
import importlib.util
import json
from pathlib import Path
import hashlib

HERE = Path(__file__).resolve().parent
helper = HERE.parent / "centroid_feasibility_2026-10-11/run_study.py"
spec = importlib.util.spec_from_file_location("r07_interval_helper", helper)
arith = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arith)
I = arith.I


def sqrt_enclosure(value):
    value = I(value)
    with localcontext() as ctx:
        ctx.prec = arith.PREC
        ctx.rounding = ROUND_HALF_EVEN
        return I(value.lo.sqrt().next_minus(), value.hi.sqrt().next_plus())


def evaluate():
    data = json.loads((HERE / "existing_audit.json").read_text())
    controls = {"Gamma6": {"delta_eV": "0.000002504", "leakage": "0.000000000001842"},
                "Gamma8": {"delta_eV": "0.000004216", "leakage": "0.000000000003466"}}
    for name, control in controls.items():
        source = data["sectors"][name]
        assert Decimal(control["delta_eV"]) >= Decimal(str(source["maximum_matched_edge_displacement_eV"]))
        assert Decimal(control["leakage"]) >= Decimal(str(source["reported_leakage_upper_exact_eigenpair_assumption"]))
    b, wmin, wmax, etamax = I("0.144882"), I("0.5"), I(5), I("0.1")
    ref = (I(str(data["sectors"]["Gamma6"]["source_edge_center_eV"])) + I(str(data["sectors"]["Gamma8"]["source_edge_center_eV"]))) / 2
    for s in data["sectors"].values():
        assert max(abs(Decimal(str(e))-ref.midpoint()) for e in s["source_edge_energies_eV"]) <= b.lo
    a = wmin/2
    floor0 = I(9)/16 * 2/arith.PI * arith.atan_interval((a-b)/etamax)
    l_constant, moment_constant = 8/(3*sqrt_enclosure(I(3))), 32/(25*sqrt_enclosure(I(5)))
    sectors = {}
    gap_budget = I(0)
    for name, control in controls.items():
        delta, epsilon = I(control["delta_eV"]), I(control["leakage"])
        max_mass_error = l_constant/wmin*delta + 2*epsilon
        floor1 = floor0-max_mass_error
        p = I(min(floor0.lo, floor1.lo))
        bound = ((1+l_constant)*delta+(2+moment_constant)*wmax*epsilon)/p
        sectors[name] = {"rounded_input_delta_eV": control["delta_eV"], "rounded_input_leakage": control["leakage"],
                         "mass_error_uniform_bound": max_mass_error.record(), "source_floor": floor0.record(),
                         "comparison_floor": floor1.record(), "centroid_transfer_error_bound_eV": bound.record()}
        gap_budget = gap_budget+bound
    return {"claim_status": "PROVEN UNDER ASSUMPTIONS / CALCULATED conditional exact-input reference envelope only",
            "eta_domain_eV": "0<eta<=0.1", "window_half_width_domain_eV": ["0.5", "5"],
            "reference_r_native_eV": ref.record(), "sectors": sectors,
            "ordering_transfer_error_bound_eV": gap_budget.record(),
            "minimum_conditional_mass_floor": str(min(Decimal(s["comparison_floor"]["lo"]) for s in sectors.values())),
            "new_native_computation": False, "physical_xc": None,
            "native_exact_eigenpair_metric_assumption_certified": False,
            "material_error_bound_eV": None, "impurity_response_error_bound_eV": None,
            "source_audit_sha256": hashlib.sha256((HERE/"existing_audit.json").read_bytes()).hexdigest(),
            "interval_helper_sha256": hashlib.sha256(helper.read_bytes()).hexdigest(),
            "evaluator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == "__main__":
    path = HERE/"reference_bound.json"
    if path.exists():
        raise FileExistsError("never overwrite a research result")
    result = evaluate()
    path.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in ("minimum_conditional_mass_floor", "ordering_transfer_error_bound_eV", "material_error_bound_eV")}, indent=2))
