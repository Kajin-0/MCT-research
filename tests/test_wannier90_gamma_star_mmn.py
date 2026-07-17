import json
from pathlib import Path

import numpy as np

from tools.check_wannier90_gamma_star_mmn import read_mmn, validate


SPEC = Path("first_principles/a0/cdte_static_kane_method_smoke.json")


def test_gamma_star_mmn_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "star.mmn"
    with path.open("w", encoding="utf-8") as stream:
        stream.write("synthetic\n2 13 1\n")
        for source in range(1, 14):
            stream.write(f"{source} 1 0 0 0\n")
            matrix = np.eye(2) if source == 1 else np.array([[1, 2j], [3, 4]])
            for n in range(2):
                for m in range(2):
                    value = matrix[m, n]
                    stream.write(f"{value.real} {value.imag}\n")

    nbnd, nk, nntot, blocks = read_mmn(path)
    assert (nbnd, nk, nntot, len(blocks)) == (2, 13, 1, 13)
    summary = validate(path, expected_bands=2)
    assert summary["gamma_self_maximum_absolute_residual"] == 0.0
    assert summary["fixed_reference_orientation"] == "S_i=M_i.conjugate_transpose"


def test_static_kane_export_contract() -> None:
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    points = spec["k_stencil"]["ordered_points"]
    win = spec["wavefunction_overlap_export"]["wannier90_win"]
    export = spec["wavefunction_overlap_export"]["pw2wannier90"]
    rendered = spec["rendered_inputs"]

    assert len(points) == 13
    assert [point["index"] for point in points] == list(range(1, 14))
    assert points[0]["label"] == "Gamma"
    assert points[-4]["label"] == "+110_h"
    assert points[-1]["label"] == "-110_h_over_2"
    assert win["num_wann"] == 8
    assert win["projection_count_after_spinor_expansion"] == 8
    assert len(win["export_only_parser_projections"]) == 4
    assert export["write_mmn"] is True
    assert export["write_amn"] is False
    assert rendered["status"] == "committed_planning_inputs_not_execution_evidence"
    assert len(rendered["file_sha256"]) == 4
    assert spec["readiness"]["rendered_inputs_committed"] is True
    assert spec["readiness"]["runtime_available"] is False
    assert spec["readiness"]["ready_for_execution"] is False
