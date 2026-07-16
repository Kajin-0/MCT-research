from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

import tools.acquire_cdte_pseudopotentials as acquire_module

UPF = b'''<UPF version="2.0.1">
<PP_HEADER element="Cd" functional="PBE" pseudo_type="NC"
 relativistic="full" has_so="T" core_correction="T" z_valence="20.0"
 l_max="2" number_of_wfc="6" number_of_proj="10"
 generated="synthetic test" />
</UPF>
'''

PSP8 = b'''Cd ONCVPSP-3.3.0
48.0 20.0 180423 zatom,zion,pspd
8 11 2 4 600 0 pspcod,pspxc,lmax,lloc,mmax,r2well
6.0 6.0 0.0 rchrg fchrg qchrg
2 4 4 0 nproj
3 1 extension_switch
4 4 0 nprojso
0 0.0 0.0
1 0.0 0.0
'''


def _selection(tmp_path: Path, *, bad_blob: bool = False) -> Path:
    blob = acquire_module.git_blob_sha1(UPF)
    value = {
        "upstream": {
            "repository": "example/pseudos",
            "commit": "0123456789abcdef",
        },
        "elements": {
            "Cd": {
                "upf_path": "Cd/Cd.upf",
                "upf_git_blob_sha1": "0" * 40 if bad_blob else blob,
                "psp8_path": "Cd/Cd.psp8",
                "psp8_git_blob_sha1": acquire_module.git_blob_sha1(PSP8),
                "psp8_pseudodojo_md5": hashlib.md5(PSP8).hexdigest(),
                "z_valence": 20,
            }
        },
    }
    path = tmp_path / "selection.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_git_blob_identity_uses_git_header() -> None:
    assert acquire_module.git_blob_sha1(b"abc") == hashlib.sha1(b"blob 3\0abc").hexdigest()


def test_acquire_verifies_and_writes_manifest(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_download(url: str, timeout_seconds: float) -> bytes:
        assert timeout_seconds == 7.0
        return UPF if url.endswith("Cd.upf") else PSP8

    monkeypatch.setattr(acquire_module, "_download", fake_download)
    manifest = acquire_module.acquire(
        _selection(tmp_path),
        tmp_path / "pseudos",
        tmp_path / "manifest.json",
        timeout_seconds=7.0,
    )

    assert manifest["acquisition_complete"] is True
    assert manifest["calculation_executed"] is False
    assert manifest["files"]["Cd_upf"]["sha256"] == hashlib.sha256(UPF).hexdigest()
    assert manifest["files"]["Cd_psp8"]["md5"] == hashlib.md5(PSP8).hexdigest()
    assert (tmp_path / "pseudos/Cd.upf").read_bytes() == UPF
    assert json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8")) == manifest


def test_acquire_fails_on_blob_mismatch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        acquire_module,
        "_download",
        lambda url, timeout_seconds: UPF if url.endswith("Cd.upf") else PSP8,
    )
    with pytest.raises(ValueError, match="Git blob mismatch"):
        acquire_module.acquire(
            _selection(tmp_path, bad_blob=True),
            tmp_path / "pseudos",
            tmp_path / "manifest.json",
        )
