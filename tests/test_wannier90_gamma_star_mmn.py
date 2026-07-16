from pathlib import Path

import numpy as np

from tools.check_wannier90_gamma_star_mmn import read_mmn, validate


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
