"""Read-only, standard-library replay of archived R07/R08 spectral evidence.

No QE, HDF5, MPI, network, fitted alloy coefficients, or data modification.
The source CSVs are actual 352-band PBE+SOC projected spectra for two
ordered xCd=0.25 configurations, not a random-alloy ensemble.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIR = ROOT / "research/programs/microscopic_bandgap/pair_environment_2026-10-15"
R08 = ROOT / "research/programs/microscopic_ionic_scattering"
MEMBERS = ("shared", "unshared")
SECTORS = ("Gamma6", "Gamma8")


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_spectra(directory: Path = PAIR) -> dict:
    spectra = {}
    for member in MEMBERS:
        spectra[member] = {}
        for sector in SECTORS:
            path = directory / f"{member}_{sector}_spectrum.csv"
            with path.open(newline="", encoding="utf-8") as handle:
                records = list(csv.DictReader(handle))
            if len(records) != 352:
                raise ValueError(f"{path}: expected 352 actual native bands")
            bands = [int(v["band_1based"]) for v in records]
            if bands != list(range(1, 353)):
                raise ValueError(f"{path}: nonconsecutive bands")
            sample = tuple(
                (float(v["energy_minus_own_Fermi_eV"]),
                 float(v["fixed_native50_host_weight_div_dimension"]))
                for v in records
            )
            if not all(math.isfinite(e) and math.isfinite(w) and w >= 0
                       for e, w in sample):
                raise ValueError(f"{path}: invalid energy or projector weight")
            weight_sum = math.fsum(w for _, w in sample)
            if not 0 < weight_sum <= 1 + 1e-10:
                raise ValueError(f"{path}: unnormalized projector trace")
            spectra[member][sector] = sample
        energies_6 = [e for e, _ in spectra[member]["Gamma6"]]
        energies_8 = [e for e, _ in spectra[member]["Gamma8"]]
        if energies_6 != energies_8:
            raise ValueError(f"{member}: sector energy grids do not match")
    return spectra


def gaussian_centroid(spectrum, width_eV: float, shift_eV: float = 0.0) -> float:
    """Normalized Gaussian-window centroid relative to chosen probe center."""
    if width_eV <= 0:
        raise ValueError("width must be positive")
    terms = [
        (e - shift_eV, w * math.exp(-0.5 * ((e - shift_eV) / width_eV) ** 2))
        for e, w in spectrum
    ]
    mass = math.fsum(weight for _, weight in terms)
    if mass <= 0:
        raise ValueError("zero observable spectral mass")
    return math.fsum(t * weight for t, weight in terms) / mass


def gaussian_contrast(spectra, width_eV: float, shift_eV: float) -> float:
    def order(member):
        return (
            gaussian_centroid(spectra[member]["Gamma6"], width_eV, shift_eV)
            - gaussian_centroid(spectra[member]["Gamma8"], width_eV, shift_eV)
        )
    return order("shared") - order("unshared")


def inverse_real(spectrum, eta_eV: float) -> float:
    """Real part of inverse scalar Stieltjes transform at z=i*eta."""
    if eta_eV <= 0:
        raise ValueError("eta must be positive")
    gr = math.fsum(-w * e / (e * e + eta_eV * eta_eV) for e, w in spectrum)
    gi = math.fsum(-w * eta_eV / (e * e + eta_eV * eta_eV) for e, w in spectrum)
    if gr * gr + gi * gi == 0:
        raise ValueError("singular scalar transform")
    return gr / (gr * gr + gi * gi)


def inverse_contrast(spectra, eta_eV: float) -> float:
    """The archived convention: Re[1/G8] - Re[1/G6], shared minus unshared."""
    def order(member):
        return (
            inverse_real(spectra[member]["Gamma8"], eta_eV)
            - inverse_real(spectra[member]["Gamma6"], eta_eV)
        )
    return order("shared") - order("unshared")


def bracketed_zero(spectra, width_eV: float, lower=-0.5, upper=0.5):
    """Central-value zero only, NEVER a physical x_c or material root."""
    f_lo = gaussian_contrast(spectra, width_eV, lower)
    f_hi = gaussian_contrast(spectra, width_eV, upper)
    if f_lo * f_hi >= 0:
        return None
    for _ in range(60):
        mid = (lower + upper) / 2
        f_mid = gaussian_contrast(spectra, width_eV, mid)
        if f_mid * f_lo <= 0:
            upper = mid
        else:
            lower, f_lo = mid, f_mid
    return (lower + upper) / 2


def replay_r07(spectra, original: dict) -> dict:
    rows = original["Gaussian_rows"]
    inv = original["scalar_causal_rows"]
    if len(rows) != 15 or len(inv) != 3:
        raise ValueError("unexpected archived sensitivity table dimensions")
    max_gaussian_error = max(
        abs(gaussian_contrast(spectra, r["W_eV"],
                              r["common_displacement_from_own_Fermi_eV"])
            - r["delta_shared_minus_unshared_eV"])
        for r in rows
    )
    max_inverse_error = max(
        abs(inverse_contrast(spectra, r["eta_eV"]) - r["delta_eV"])
        for r in inv
    )
    if max_gaussian_error >= 1e-11 or max_inverse_error >= 1e-11:
        raise AssertionError("independent CSV replay differs from archived result")

    negative = next(r for r in rows if r["W_eV"] == 1
                    and r["common_displacement_from_own_Fermi_eV"] == -0.5)
    positive = next(r for r in rows if r["W_eV"] == 1
                    and r["common_displacement_from_own_Fermi_eV"] == 0.5)
    # These bounds cover ONLY archived projector/tail/arithmetic terms.
    if not (negative["conditional_interval_eV"][1] < 0
            and positive["conditional_interval_eV"][0] > 0):
        raise AssertionError("opposite conditional sign certifications failed")

    values = [inverse_contrast(spectra, r["eta_eV"]) for r in inv]
    roots = {str(width): bracketed_zero(spectra, width)
             for width in (1.0, 1.5, 2.0)}
    return {
        "status": "RETAINED_SPECTRA_REPLAY_PASS",
        "n_spectra": 4,
        "bands_per_spectrum": 352,
        "gaussian_rows_replayed": len(rows),
        "inverse_rows_replayed": len(inv),
        "max_gaussian_replay_error_eV": max_gaussian_error,
        "max_inverse_replay_error_eV": max_inverse_error,
        "inverse_eta_eV": [r["eta_eV"] for r in inv],
        "inverse_shared_minus_unshared_meV": [1000 * v for v in values],
        "inverse_eta_span_meV": 1000 * (max(values) - min(values)),
        "inverse_span_pct_of_mean_magnitude":
            100 * (max(values) - min(values)) / abs(math.fsum(values) / len(values)),
        "W1_gaussian_shift_minus0p5_meV":
            1000 * gaussian_contrast(spectra, 1, -0.5),
        "W1_gaussian_shift_plus0p5_meV":
            1000 * gaussian_contrast(spectra, 1, 0.5),
        "W1_opposite_signs_within_archived_conditional_bounds": True,
        "W1_shift_minus0p5_archived_interval_meV":
            [1000 * v for v in negative["conditional_interval_eV"]],
        "W1_shift_plus0p5_archived_interval_meV":
            [1000 * v for v in positive["conditional_interval_eV"]],
        "gaussian_central_probe_shift_zero_eV": roots,
        "scope": "fixed-reference, own-Fermi, finite-352-band PBE ordered cells",
        "not_material_gap_or_disorder_ensemble": True,
    }


def replay_r08(original: dict) -> dict:
    records = original["records"]
    if len(records) != 16:
        raise ValueError("expected eight k entries times two initial sectors")
    by_key = {}
    for item in records:
        key = (item["k_index"], item["sector"])
        if key in by_key:
            raise ValueError("duplicate k-sector")
        by_key[key] = item
        for seg in item["segments"].values():
            residual = (
                seg["local_eV2_per_initial"]
                + seg["nonlocal_eV2_per_initial"]
                + seg["interference_eV2_per_initial"]
                - seg["total_eV2_per_initial"]
            )
            if abs(residual) > 1e-9:
                raise AssertionError("bare-ionic interference identity broken")
    remote_fraction = {}
    for sector in ("Gamma6_like", "Gamma8_like"):
        row = by_key[(8, sector)]["segments"]
        remote_fraction[sector] = (
            row["remote"]["total_eV2_per_initial"]
            / row["all"]["total_eV2_per_initial"]
        )
    non_gamma_near = {
        sector: [
            (k, by_key[(k, sector)]["segments"]["near"]["final_band_count"])
            for k in range(2, 9)
            if by_key[(k, sector)]["segments"]["near"]["final_band_count"] > 0
        ] for sector in ("Gamma6_like", "Gamma8_like")
    }
    return {
        "status": "COMMITTED_SUMMARY_IDENTITY_CHECK_PASS",
        "n_k_sector_records": len(records),
        "remote_gt5eV_fraction_at_k8": remote_fraction,
        "non_gamma_saved_k_with_near_0p5eV_final_bands": non_gamma_near,
        "source_raw_packet_sha256": original["source_raw_sha256"],
        "raw_packet_independently_replayed": False,
        "not_screened_on_shell_linewidth": True,
    }


def run() -> dict:
    spectra = load_spectra()
    return {
        "r07": replay_r07(spectra, _json(PAIR / "numerical_result.json")),
        "r08": replay_r08(_json(R08 / "finite_k_interference_summary.json")),
        "publication_gate": "NO_GO_PHYSICAL_DISORDER_CORRECTION",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compact", action="store_true",
                        help="print one-line JSON instead of indented output")
    args = parser.parse_args()
    print(json.dumps(run(), indent=None if args.compact else 2,
                     sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
