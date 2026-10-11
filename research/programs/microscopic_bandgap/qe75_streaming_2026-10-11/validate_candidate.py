"""Bounded compile/link/unit validation; never invokes PW or MPI.

Run from DFT after sourcing scripts/env.sh. --link-only builds an explicitly
UNVALIDATED private executable; it is never executed or installed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

HERE = Path(__file__).resolve().parent
NEGATIVE = {
    "missing": "missing producer vectors", "duplicate": "duplicate producer vector",
    "unsealed": "sealed generation", "sealed_write": "unsealed open generation",
    "q_range": "q outside store", "plane_shape": "plane shape mismatch",
    "truncate": "read:", "shape": "invalid store shape",
    "preexisting": "pre-existing stream file", "overflow": "64-bit storage offset overflow",
}


def run(cmd, cwd, timeout=180):
    started = time.monotonic()
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout,
                       env={**os.environ, "OMP_NUM_THREADS": "1"})
    return {"command": [str(v) for v in cmd], "returncode": p.returncode,
            "stdout": p.stdout, "stderr": p.stderr, "wall_seconds": time.monotonic()-started}


def body(text, start, end):
    i = text.index(start)
    j = text.index(end, i) + len(end)
    return text[i:j]


def audit_sources(source):
    old = subprocess.check_output(["git", "show", "HEAD:PW/src/exx.f90"], cwd=source, text=True)
    new = (source/"PW/src/exx.f90").read_text()
    checks = {}
    for start, end, declaration in [
        ("  SUBROUTINE vexx_k(", "  END SUBROUTINE vexx_k", "    INTEGER :: ibnd, ik, im , ikq, iq, ipol"),
        ("  FUNCTION exxenergy2_k(", "  END FUNCTION  exxenergy2_k", "                ik, ikk, ig, ikq, iq, ir"),
    ]:
        original = body(old, start, end)
        modified = body(new, start, end)
        assert modified.count("CALL qs_load(qstore,ikq,exxbuff(:,:,1))") == 1
        # Independent operation-sequence comparison, not the patcher's subscript parser.
        # Remove ONLY the new I/O, local storage alias and declaration. Every other
        # byte must agree. A missed continued rhoc read leaves ',ikq)' after this
        # inverse mapping and is caught by the required source-buffer count.
        buffer_mentions = modified.count("exxbuff(")
        buffer_aliases = len(re.findall(r"exxbuff\([^!]*?\biqbuf\)", modified))
        assert buffer_aliases == buffer_mentions - 1, (start, buffer_aliases, buffer_mentions)
        stripped = re.sub(r"#if defined\(__EXX_QSTREAM\)\n.*?#endif\n", "", modified, flags=re.S)
        stripped = stripped.replace(declaration+", iqbuf", declaration)
        stripped = re.sub(r"^\s*iqbuf=ikq\n", "", stripped, flags=re.M)
        stripped = stripped.replace("iqbuf", "ikq")
        assert stripped == original, start
        checks[start.strip()] = {"all_source_reads_mapped": True,
                                "all_other_operations_and_global_indices_unchanged": True,
                                "buffer_mentions_with_loader": buffer_mentions}
    # ACE factorization/projectors and all GPU/localized routines remain stock.
    for start, end in [
        ("  SUBROUTINE aceinit(", "  END SUBROUTINE aceinit"),
        ("  SUBROUTINE aceinit_k(", "  END SUBROUTINE aceinit_k"),
        ("  SUBROUTINE aceupdate_k(", "  END SUBROUTINE aceupdate_k"),
        ("  SUBROUTINE vexxace_k(", "  END SUBROUTINE vexxace_k"),
        ("  SUBROUTINE vexx_loc_k(", "  END SUBROUTINE vexx_loc_k"),
    ]:
        assert body(old,start,end) == body(new,start,end)
        checks[start.strip()] = {"byte_identical": True}
    assert "nproc_orthopool = npool" in (source/"Modules/mp_pools.f90").read_text()
    checks["singleton_orthopool"] = {"source_definition_checked": True, "requires_npool": 1}
    return checks


def validate(private, link_only=False):
    private = private.resolve()
    dft = Path("/home/User/opencode_workspace/DFT").resolve()
    assert private.is_relative_to(dft/".local")
    source=private/"q-e"; env=dft/".local/qe-env"
    fc=private/"toolchain/bin/x86_64-conda-linux-gnu-gfortran"
    report={"native_executables_invoked": False, "qualified_for_native_run": False,
            "source_audit": audit_sources(source), "compiles": [], "unit_cases": [], "link": None}
    includes=[]
    for d in sorted((env/"include/qe").iterdir()):
        if d.is_dir(): includes += ["-I",str(d)]
    includes += ["-I",str(env/"include")]
    flags=["-cpp","-D__MPI","-D__HDF5","-D__SCALAPACK","-D__ELPA","-fopenmp",
           "-ffree-line-length-none","-fallow-argument-mismatch","-O0","-g","-fcheck=all",
           "-fcheck=array-temps","-ffunction-sections","-fdata-sections"]
    for mode in ["stream","stock"]:
        out=private/(mode+"-objects"); out.mkdir(exist_ok=True)
        for name in ["exx_qstream","exx","electrons"]:
            cmd=["/usr/bin/time","-v",str(fc),*flags,*(["-D__EXX_QSTREAM"] if mode=="stream" else []),
                 "-J",str(out),"-I",str(out),*includes,"-c",str(source/f"PW/src/{name}.f90"),"-o",str(out/f"{name}.o")]
            result=run(cmd,dft)
            result.update({"mode":mode,"unit":name})
            report["compiles"].append(result)
            assert result["returncode"] == 0, result
    out=private/"unit-tests"; out.mkdir(exist_ok=True)
    for optimization in ["-O0","-O2"]:
        exe=out/("store_kernel_test"+optimization)
        result=run([str(fc),optimization,"-fcheck=all","-fcheck=array-temps","-fbacktrace",
                    "-ffree-line-length-none","-fopenmp","-J",str(out),*includes,
                    str(HERE/"exx_qstream.f90"),str(HERE/"store_kernel_test.f90"),"-o",str(exe)],dft)
        assert result["returncode"] == 0, result
        report["compiles"].append({**result,"unit":"unit_test", "optimization":optimization})
        for mode in ["normal","extent64",*NEGATIVE]:
            path=out/(mode+optimization+".bin")
            assert not path.exists(), path
            result=run([str(exe),mode,str(path)],dft,timeout=20)
            if mode in NEGATIVE:
                passed=result["returncode"] == 9 and NEGATIVE[mode] in result["stdout"]
            else:
                passed=result["returncode"] == 0 and ("STORE_KERNEL_PASS" if mode=="normal" else "EXTENT64_PASS") in result["stdout"]
            result.update({"case":mode,"optimization":optimization,"passed":passed})
            report["unit_cases"].append(result)
            if path.exists(): path.unlink()
            assert passed, result
            assert "array temporary" not in result["stderr"].lower()
    if link_only:
        out=private/"link-only"; out.mkdir(exist_ok=True)
        result=run([str(fc),*flags,"-J",str(out),*includes,"-c",str(source/"PW/src/pwscf.f90"),"-o",str(out/"pwscf.o")],dft)
        assert result["returncode"] == 0, result
        report["compiles"].append({**result,"unit":"pwscf_main"})
        qelib=env/"lib"; archive=out/"libqe_pw_candidate.a"; shutil.copy2(qelib/"libqe_pw.a",archive)
        subprocess.run(["/usr/bin/ar","d",str(archive),"exx.f90.o","electrons.f90.o"],check=True)
        for name in ["exx_qstream","exx","electrons"]:
            shutil.copy2(private/"stream-objects"/f"{name}.o",out/f"{name}.f90.o")
        subprocess.run(["/usr/bin/ar","r",str(archive),*[str(out/f"{n}.f90.o") for n in ["exx_qstream","exx","electrons"]]],check=True)
        libs=["device_lapack","lax","kssolver_davidson","kssolver_cg","kssolver_paro","kssolver_rmmdiis","kssolver_dense",
              "upflib","modules","modules_c","fftx","fftx_c","dftd3","xclib","libbeef","devxlib","xml","utilx","utilx_c"]
        exe=out/"pw.qstream.UNVALIDATED"
        cmd=[str(fc),"-fopenmp",str(out/"pwscf.o"),"-Wl,--start-group",str(archive),*[str(qelib/f"libqe_{n}.a") for n in libs],
             str(qelib/"libmbd.a"),"-Wl,--end-group","-L",str(qelib),"-Wl,-rpath,"+str(qelib),"-lelpa","-lscalapack",
             "-lhdf5_fortran","-lhdf5","-lfftw3","-lfftw3_omp","-lmpi_mpifh","-lmpi","-llapack","-lblas","-lm","-o",str(exe)]
        result=run(cmd,dft)
        assert result["returncode"] == 0, result
        result["sha256"]=hashlib.sha256(exe.read_bytes()).hexdigest()
        result["ldd"]=subprocess.check_output(["ldd",str(exe)],text=True)
        assert "not found" not in result["ldd"]
        report["link"]=result
    report["compiler_version"]=subprocess.check_output([str(fc),"--version"],text=True)
    report["passed"]=True
    (private/"validation.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"passed":True,"source_checks":len(report["source_audit"]),
                      "compiled_units":len(report["compiles"]),"unit_cases":len(report["unit_cases"]),
                      "private_linked":report["link"] is not None,"native_run_qualified":False},indent=2))


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("private_directory",type=Path)
    parser.add_argument("--link-only",action="store_true")
    args=parser.parse_args()
    validate(args.private_directory,args.link_only)
