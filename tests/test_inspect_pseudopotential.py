from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from tools.inspect_pseudopotential import inspect, validate


UPF = """<UPF version="2.0.1">
<PP_HEADER element="Cd" functional="PBE" pseudo_type="NC"
 relativistic="full" has_so="T" core_correction="T" z_valence="20.0"
 l_max="2" number_of_wfc="6" number_of_proj="10"
 generated="synthetic test" />
</UPF>
"""

PSP8 = """Cd ONCVPSP-3.3.0
48.0 20.0 180423 zatom,zion,pspd
8 11 2 4 600 0 pspcod,pspxc,lmax,lloc,mmax,r2well
6.0 6.0 0.0 rchrg fchrg qchrg
2 4 4 0 nproj
3 1 extension_switch
4 4 0 nprojso
0 0.0 0.0
1 0.0 0.0
"""


def test_inspect_upf_and_hashes(tmp_path: Path) -> None:
    path = tmp_path / "Cd.upf"
    path.write_text(UPF, encoding="utf-8")
    metadata = inspect(path, "upf")
    assert metadata["element"] == "Cd"
    assert metadata["functional"] == "PBE"
    assert metadata["fully_relativistic"] is True
    assert metadata["spin_orbit"] is True
    assert metadata["nonlinear_core_correction"] is True
    assert metadata["z_valence"] == 20.0
    assert metadata["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()

    validate(
        metadata,
        expected_element="Cd",
        expected_z_valence=20.0,
        expected_functional="PBE",
        expected_pspxc=None,
        require_fully_relativistic=True,
        require_spin_orbit=True,
        require_nlcc=True,
    )


def test_inspect_psp8_relativistic_extension(tmp_path: Path) -> None:
    path = tmp_path / "Cd.psp8"
    path.write_text(PSP8, encoding="utf-8")
    metadata = inspect(path, "psp8")
    assert metadata["element"] == "Cd"
    assert metadata["pspcod"] == 8
    assert metadata["pspxc"] == 11
    assert metadata["fully_relativistic"] is True
    assert metadata["spin_orbit"] is True
    assert metadata["spin_orbit_projectors"] == [4, 4, 0]

    validate(
        metadata,
        expected_element="Cd",
        expected_z_valence=20.0,
        expected_functional=None,
        expected_pspxc=11,
        require_fully_relativistic=True,
        require_spin_orbit=True,
        require_nlcc=False,
    )


def test_validation_fails_closed_on_wrong_element(tmp_path: Path) -> None:
    path = tmp_path / "Cd.upf"
    path.write_text(UPF, encoding="utf-8")
    metadata = inspect(path, "upf")
    with pytest.raises(ValueError, match="expected 'Te'"):
        validate(
            metadata,
            expected_element="Te",
            expected_z_valence=20.0,
            expected_functional="PBE",
            expected_pspxc=None,
            require_fully_relativistic=True,
            require_spin_orbit=True,
            require_nlcc=True,
        )
