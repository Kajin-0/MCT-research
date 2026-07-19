#!/usr/bin/env python3
"""Generate editable IRPT LaTeX tables from the frozen manuscript CSV records."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

TABLE_FILENAMES = (
    "table1_specimen_provenance.tex",
    "table2_candidate_definitions.tex",
    "table3_edge_ensemble.tex",
    "table4_material_model_comparison.tex",
    "table5_claim_boundaries.tex",
)

MODEL_LABELS = {
    "hansen": "Hansen",
    "published_seiler": "Seiler 1990",
    "laurenti": "Laurenti",
    "provisional_hansen_pade": "Provisional Hansen--Pade",
}

CANDIDATE_LABELS = {
    "fractional_power_free": "fractional power, fitted $p$",
    "fractional_power_fixed": "fractional power, fixed $p$",
    "fractional_power_p_0.5": "fractional $p=0.5$",
    "fractional_power_p_0.7": "fractional $p=0.7$",
    "fractional_power_p_0.872": "fractional $p=0.872$",
    "fractional_power_p_0.849": "fractional $p=0.849$",
    "fractional_power_p_1": "fractional $p=1$",
    "chu_1994_kane_region": "Chu 1994 Kane region",
    "fixed_absorption_threshold": "fixed absorption threshold",
}

CLASS_LABELS = {
    "fitted_absorption_model": "fitted model",
    "fixed_absorption_threshold": "fixed threshold",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def latex_escape(value: Any) -> str:
    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(character, character) for character in text)


def specimen_x(specimen_id: str) -> str:
    return specimen_id.rsplit("x", 1)[-1]


def candidate_label(identifier: str) -> str:
    if identifier in CANDIDATE_LABELS:
        return CANDIDATE_LABELS[identifier]
    if identifier.startswith("threshold_"):
        threshold = identifier.removeprefix("threshold_").removesuffix("_cm-1")
        return rf"$\alpha={threshold}$~cm$^{{-1}}$"
    raise ValueError(f"unsupported candidate identifier: {identifier}")


def source_panel(source: str) -> str:
    if "Figure 6a" in source:
        return "Moazzami 2005, Fig.~6a"
    if "Figure 6b" in source:
        return "Moazzami 2005, Fig.~6b"
    raise ValueError(f"unsupported source locator: {source}")


def table1(rows: list[dict[str, str]]) -> str:
    body = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Specimen and measurement provenance for the two real-spectrum records. Blank composition uncertainty and unknown carrier state are retained as missing metadata rather than inferred. Full source and input hashes remain in the frozen CSV record.}",
        r"\label{tab:specimen-provenance}",
        r"\begin{tabular}{lllllll}",
        r"\toprule",
        r"$x$ & $T$ (K) & Thickness ($\mu$m) & Points & $\sigma_x$ & Carrier state & Source \\",
        r"\midrule",
    ]
    for row in rows:
        sigma = row["composition_sigma_x"] or "not reported"
        carrier = (
            f'{row["carrier_type"]}; {row["carrier_density_status"]}'
        )
        body.append(
            " & ".join(
                (
                    f'{float(row["composition_x"]):.3f}',
                    f'{float(row["temperature_k"]):.0f}',
                    f'{float(row["thickness_um"]):.2f}',
                    row["digitized_point_count"],
                    latex_escape(sigma),
                    latex_escape(carrier),
                    source_panel(row["source"]),
                )
            )
            + r" \\"
        )
    body += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    return "\n".join(body)


def table2(rows: list[dict[str, str]]) -> str:
    body = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Observation-candidate definitions and source-supported domains. Operational thresholds are not identified with the latent material gap.}",
        r"\label{tab:candidate-definitions}",
        r"\begin{tabular}{p{0.22\textwidth}p{0.39\textwidth}p{0.29\textwidth}}",
        r"\toprule",
        r"Candidate & Definition & Admissible domain \\",
        r"\midrule",
    ]
    definitions = {
        "fractional_power_free": r"$\alpha=A(E-E_g)^p/E$; $p$ fitted",
        "fractional_power_fixed": r"$\alpha=A(E-E_g)^p/E$; $p$ fixed",
        "chu_1994_kane_region": r"$\alpha=\alpha_g\exp[\sqrt{\beta(x,T)(E-E_g)}]$",
        "fixed_absorption_threshold": r"First interpolated $\alpha$ crossing",
    }
    domains = {
        "fractional_power_free": "declared fit window",
        "fractional_power_fixed": r"$p=0.5$, $0.7$, source-panel $p$, and $1.0$",
        "chu_1994_kane_region": r"$0.170\leq x\leq0.443$; $77\leq T\leq300$~K",
        "fixed_absorption_threshold": r"400--5000~cm$^{-1}$; 5000 flagged when coordinate-sensitive",
    }
    for row in rows:
        identifier = row["candidate_id"]
        body.append(
            f"{candidate_label(identifier)} & {definitions[identifier]} & "
            f"{domains[identifier]} \\\\"
        )
    body += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    return "\n".join(body)


def table3(rows: list[dict[str, str]]) -> str:
    body = [
        r"\begingroup",
        r"\small",
        r"\setlength{\tabcolsep}{3.5pt}",
        r"\begin{longtable}{p{0.055\textwidth}p{0.20\textwidth}p{0.105\textwidth}rrrrp{0.16\textwidth}}",
        r"\caption{Complete extracted-edge ensemble. Coordinate shift is the maximum absolute shift over the declared coherent digitization perturbations. Boundary-limited candidates are retained but are not treated as identified edges.}\label{tab:edge-ensemble}\\",
        r"\toprule",
        r"$x$ & Candidate & Class & Edge (meV) & Bound & Shift (meV) & Margin (meV) & Nominal closest comparator \\",
        r"\midrule",
        r"\endfirsthead",
        r"\multicolumn{8}{c}{\tablename\ \thetable{} -- continued}\\",
        r"\toprule",
        r"$x$ & Candidate & Class & Edge (meV) & Bound & Shift (meV) & Margin (meV) & Nominal closest comparator \\",
        r"\midrule",
        r"\endhead",
        r"\midrule",
        r"\multicolumn{8}{r}{Continued on next page}\\",
        r"\endfoot",
        r"\bottomrule",
        r"\endlastfoot",
    ]
    previous_specimen = None
    for row in rows:
        specimen = row["specimen_id"]
        if previous_specimen is not None and specimen != previous_specimen:
            body.append(r"\addlinespace")
        previous_specimen = specimen
        boundary = "yes" if row["boundary_limited"] == "True" else "no"
        body.append(
            " & ".join(
                (
                    specimen_x(specimen),
                    candidate_label(row["candidate_id"]),
                    CLASS_LABELS[row["observation_class"]],
                    f'{float(row["edge_mev"]):.3f}',
                    boundary,
                    f'{float(row["digitization_coordinate_shift_mev"]):.3f}',
                    f'{float(row["nominal_winner_margin_mev"]):.3f}',
                    MODEL_LABELS[row["nominal_winner"]],
                )
            )
            + r" \\"
        )
    body += [r"\end{longtable}", r"\endgroup", ""]
    return "\n".join(body)


def table4(rows: list[dict[str, str]]) -> str:
    body = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Material-gap predictions and fitted observation-model residual intervals. Residual is extracted edge minus model prediction. Strict material-law ranking is not authorized for either specimen.}",
        r"\label{tab:model-comparison}",
        r"\begin{tabular}{lllll}",
        r"\toprule",
        r"$x$ & Comparator & Prediction (meV) & Fitted residual interval (meV) & Strict rank \\",
        r"\midrule",
    ]
    previous_specimen = None
    for row in rows:
        specimen = row["specimen_id"]
        if previous_specimen is not None and specimen != previous_specimen:
            body.append(r"\addlinespace")
        previous_specimen = specimen
        interval = (
            f'[{float(row["fitted_model_residual_min_mev"]):.3f}, '
            f'{float(row["fitted_model_residual_max_mev"]):.3f}]'
        )
        body.append(
            " & ".join(
                (
                    specimen_x(specimen),
                    MODEL_LABELS[row["model_id"]],
                    f'{float(row["prediction_mev"]):.3f}',
                    interval,
                    "no",
                )
            )
            + r" \\"
        )
    body += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    return "\n".join(body)


def table5(rows: list[dict[str, str]]) -> str:
    body = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Claim and evidence boundary for the present manuscript.}",
        r"\label{tab:claim-boundaries}",
        r"\begin{tabular}{p{0.40\textwidth}p{0.15\textwidth}p{0.35\textwidth}}",
        r"\toprule",
        r"Claim & Status & Evidence boundary \\",
        r"\midrule",
    ]
    statuses = {
        "authorized": "authorized",
        "descriptive only": "descriptive only",
        "authorized through 4000 cm-1": r"authorized through 4000~cm$^{-1}$",
        "not authorized": "not authorized",
    }
    for row in rows:
        claim = latex_escape(row["claim"]).replace("6-7", "6--7")
        boundary = latex_escape(row["boundary"])
        boundary = boundary.replace("300 K", "300~K")
        boundary = boundary.replace("0.18-0.25", "0.18--0.25")
        body.append(
            f'{claim} & {statuses[row["status"]]} & {boundary} \\\\'
        )
    body += [r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""]
    return "\n".join(body)


def build(repository_root: str | Path, output_dir: str | Path) -> list[Path]:
    root = Path(repository_root)
    source = root / "manuscript/observation_model_uncertainty"
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    builders = (
        ("table1_specimen_provenance.csv", TABLE_FILENAMES[0], table1),
        ("table2_candidate_definitions.csv", TABLE_FILENAMES[1], table2),
        ("table3_edge_ensemble.csv", TABLE_FILENAMES[2], table3),
        ("table4_material_model_comparison.csv", TABLE_FILENAMES[3], table4),
        ("table5_claim_boundaries.csv", TABLE_FILENAMES[4], table5),
    )
    written: list[Path] = []
    for csv_name, tex_name, renderer in builders:
        target = output / tex_name
        target.write_text(renderer(read_csv(source / csv_name)), encoding="utf-8")
        written.append(target)
    return written


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--output-dir", required=True)
    arguments = parser.parse_args()
    for path in build(arguments.repository_root, arguments.output_dir):
        print(path)


if __name__ == "__main__":
    main()
