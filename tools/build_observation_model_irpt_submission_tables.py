#!/usr/bin/env python3
"""Build width-constrained IRPT submission tables from frozen manuscript CSVs."""
from __future__ import annotations

import argparse
from pathlib import Path

from tools.build_observation_model_irpt_tables import (
    MODEL_LABELS,
    TABLE_FILENAMES,
    candidate_label,
    latex_escape,
    read_csv,
    source_panel,
    specimen_x,
    table2,
    table5,
)

CLASS_LABELS = {
    "fitted_absorption_model": "fit",
    "fixed_absorption_threshold": "threshold",
}


def table1(rows: list[dict[str, str]]) -> str:
    body = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\small",
        r"\setlength{\tabcolsep}{3pt}",
        r"\caption{Specimen and measurement provenance for the two real-spectrum records. Blank composition uncertainty and unknown carrier state are retained as missing metadata rather than inferred. Full source and input hashes remain in the frozen CSV record.}",
        r"\label{tab:specimen-provenance}",
        r"\begin{tabularx}{\textwidth}{@{}rrrrp{0.13\textwidth}Yp{0.19\textwidth}@{}}",
        r"\toprule",
        r"$x$ & $T$ (K) & Thickness ($\mu$m) & Points & $\sigma_x$ & Carrier state & Source \\",
        r"\midrule",
    ]
    for row in rows:
        sigma = (
            latex_escape(row["composition_sigma_x"])
            if row["composition_sigma_x"]
            else r"\textemdash{}"
        )
        carrier = f'{row["carrier_type"]}; density not reported'
        body.append(
            " & ".join(
                (
                    f'{float(row["composition_x"]):.3f}',
                    f'{float(row["temperature_k"]):.0f}',
                    f'{float(row["thickness_um"]):.2f}',
                    row["digitized_point_count"],
                    sigma,
                    latex_escape(carrier),
                    source_panel(row["source"]),
                )
            )
            + r" \\"
        )
    body += [r"\bottomrule", r"\end{tabularx}", r"\end{table*}", ""]
    return "\n".join(body)


def table3(rows: list[dict[str, str]]) -> str:
    body = [
        r"\begin{landscape}",
        r"\begingroup",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{4pt}",
        r"\setlength{\LTleft}{0pt}",
        r"\setlength{\LTright}{0pt}",
        r"\begin{longtable}{@{}rp{1.85in}p{0.75in}rrrrp{1.65in}@{}}",
        r"\caption{Complete extracted-edge ensemble. Coordinate shift is the maximum absolute shift over the declared coherent digitization perturbations. Boundary-limited candidates are retained but are not treated as identified edges.}\label{tab:edge-ensemble}\\",
        r"\toprule",
        r"$x$ & Candidate & Type & Edge (meV) & Bound? & Shift (meV) & Lead (meV) & Closest comparator \\",
        r"\midrule",
        r"\endfirsthead",
        r"\multicolumn{8}{c}{\tablename\ \thetable{} -- continued}\\",
        r"\toprule",
        r"$x$ & Candidate & Type & Edge (meV) & Bound? & Shift (meV) & Lead (meV) & Closest comparator \\",
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
    body += [
        r"\end{longtable}",
        r"\endgroup",
        r"\end{landscape}",
        "",
    ]
    return "\n".join(body)


def table4(rows: list[dict[str, str]]) -> str:
    body = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\small",
        r"\setlength{\tabcolsep}{4pt}",
        r"\caption{Material-gap predictions and fitted observation-model residual intervals. Residual is extracted edge minus model prediction. Strict material-law ranking is not authorized for either specimen.}",
        r"\label{tab:model-comparison}",
        r"\begin{tabularx}{\textwidth}{@{}rYrp{0.27\textwidth}c@{}}",
        r"\toprule",
        r"$x$ & Comparator & Prediction (meV) & Fitted residual interval (meV) & Strict ranking? \\",
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
    body += [r"\bottomrule", r"\end{tabularx}", r"\end{table*}", ""]
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
