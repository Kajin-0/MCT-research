"""Apply a fail-closed candidate to a PRIVATE pristine QE 7.5 source checkout.

No build, native run, runtime installation, input modification or git commit.
Compile with -D__EXX_QSTREAM to select streaming. Default build stays stock.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import shutil
import subprocess

QE_COMMIT = "770a0b2d12928a67048e2f3da8d10d057e52179e"
EXX_SHA = "9ce3e0fa836a11f6e3d8dda36ab92c1f39082fbf0587fc56a36fcc3f88b57bdf"


def once(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, (old[:100], text.count(old))
    return text.replace(old, new, 1)


def rewrite_q_reads(block: str) -> str:
    """Parse balanced subscripts, including continued statements/nested indices.

    A line-based rewrite misses the rhoc product's continuation lines. Never
    replace global ikq on kernel/occupation/geometry expressions.
    """
    edits = []
    for match in re.finditer(r"\bexxbuff\(", block, flags=re.I):
        depth = 1
        commas = []
        for i in range(match.end(), len(block)):
            c = block[i]
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0:
                    assert len(commas) == 2
                    start, end = commas[1] + 1, i
                    argument = block[start:end]
                    q = argument.replace("&", "").strip()
                    assert q in {"ikq", "1"}, q
                    if q == "ikq":
                        edits.append((start, end, re.sub(r"\bikq\b", "iqbuf", argument)))
                    break
            elif c == "," and depth == 1:
                commas.append(i)
        else:
            raise AssertionError("unclosed exxbuff subscript")
    for start, end, replacement in reversed(edits):
        block = block[:start] + replacement + block[end:]
    return block


def candidate(root: Path) -> None:
    root = root.resolve()
    permitted = Path("/home/User/opencode_workspace/DFT/.local").resolve()
    assert root.is_relative_to(permitted), "private project-local source only"
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip() == QE_COMMIT
    assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=root, text=True), "require pristine source"
    path = root / "PW/src/exx.f90"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == EXX_SHA
    exx = path.read_text()
    exx = once(exx, "  USE kinds,                ONLY : DP\n", """  USE kinds,                ONLY : DP
#if defined(__EXX_QSTREAM)
  USE exx_qstream, ONLY : exx_qstore, qs_begin, qs_put, qs_seal, qs_load, qs_close
#endif
""")
    exx = once(exx, "  SAVE\n", """  SAVE
#if defined(__EXX_QSTREAM)
  TYPE(exx_qstore), PRIVATE :: qstore
#endif
""")
    exx = once(exx, "    IF ( ALLOCATED(exxbuff) )      DEALLOCATE( exxbuff )", """#if defined(__EXX_QSTREAM)
    CALL qs_close(qstore)
#endif
    IF ( ALLOCATED(exxbuff) )      DEALLOCATE( exxbuff )""")
    start = exx.index("  SUBROUTINE exxinit(")
    end = exx.index("  END SUBROUTINE exxinit", start)
    block = exx[start:end]
    block = once(block, "    USE io_files,             ONLY : nwordwfc, iunwfc_exx", """    USE io_files,             ONLY : nwordwfc, iunwfc_exx
#if defined(__EXX_QSTREAM)
    USE io_files,             ONLY : tmp_dir, prefix
    USE control_flags,        ONLY : lscf, restart, tstress, tprnfor
#endif""")
    block = once(block, "    INTEGER :: ibnd_exx, evc_offset", """    INTEGER :: ibnd_exx, evc_offset, iqbuf
#if defined(__EXX_QSTREAM)
    CHARACTER(1024) :: qstream_path
    CHARACTER(32) :: qstream_rank
#endif""")
    block = once(block, "    CALL start_clock ('exxinit')", """#if defined(__EXX_QSTREAM)
    ! Fail before transform/allocation; unsupported readers retain stock layout.
    IF (.NOT.lscf .OR. PRESENT(nbndproj_) .OR. restart) &
      CALL errore('exxinit','qstream requires fresh SCF; restart/non-SCF unsupported',1)
    IF (gamma_only .OR. .NOT.noncolin .OR. npol /= 2 .OR. use_gpu .OR. DoLoc .OR. .NOT.use_ace) &
      CALL errore('exxinit','qstream requires CPU nonlocalized spinor k-point ACE',1)
    IF (npool /= 1 .OR. negrp /= 1 .OR. okvan .OR. okpaw .OR. tstress .OR. tprnfor) &
      CALL errore('exxinit','qstream requires one pool/group, NC PP, no forces/stress',1)
#endif
    CALL start_clock ('exxinit')""")
    old = """      IF (.NOT. ALLOCATED(exxbuff)) THEN
         IF (gamma_only) THEN"""
    block = once(block, old, """#if defined(__EXX_QSTREAM)
      WRITE(qstream_rank,'(I0)') me_pool
      qstream_path=TRIM(tmp_dir)//'/'//TRIM(prefix)//'.exx_qstream.'//TRIM(qstream_rank)
      CALL qs_begin(qstore,TRIM(qstream_path),nrxxs*npol,ibnd_buff_start, &
                    ibnd_buff_start+max_buff_bands_per_egrp-1,nkqs)
      IF (ALLOCATED(exxbuff)) THEN
        IF (SIZE(exxbuff,1) /= nrxxs*npol .OR. SIZE(exxbuff,2) /= max_buff_bands_per_egrp .OR. &
            LBOUND(exxbuff,2) /= ibnd_buff_start .OR. SIZE(exxbuff,3) /= 1) DEALLOCATE(exxbuff)
      ENDIF
      IF (.NOT.ALLOCATED(exxbuff)) ALLOCATE(exxbuff(nrxxs*npol, &
           ibnd_buff_start:ibnd_buff_start+max_buff_bands_per_egrp-1,1))
#else
      IF (.NOT. ALLOCATED(exxbuff)) THEN
         IF (gamma_only) THEN""")
    block = once(block, "      IF (.not. allocated(exxbuff_d) .and. use_gpu) THEN", """#endif
      IF (.not. allocated(exxbuff_d) .and. use_gpu) THEN""")
    block = once(block, "                isym = ABS(index_sym(ikq) )", """                isym = ABS(index_sym(ikq) )
                iqbuf=ikq
#if defined(__EXX_QSTREAM)
                iqbuf=1
#endif""")
    # Only the four CPU spinor writes, not GPU or excluded collinear paths.
    for old in [
        "exxbuff(ir,ibnd,ikq) = psic_nc(ir,1)",
        "exxbuff(ir+nrxxs,ibnd,ikq) = psic_nc(ir,2)",
        "exxbuff(ir,ibnd,ikq) = CONJG(psic_nc(ir,2))",
        "exxbuff(ir+nrxxs,ibnd,ikq) = -CONJG(psic_nc(ir,1))",
    ]:
        block = once(block, old, old.replace(",ikq)", ",iqbuf)"))
    block = once(block, "                ENDIF ! noncolinear", """                ENDIF ! noncolinear
#if defined(__EXX_QSTREAM)
                CALL qs_put(qstore,ikq,ibnd,exxbuff(:,ibnd,1))
#endif""")
    block = once(block, "    IF ( .NOT. gamma_only ) THEN\n       DO ikq = 1, nkqs", """#if defined(__EXX_QSTREAM)
    ! npool=1 => intra_orthopool_comm is singleton; seal instead of no-op bcasts.
    CALL qs_seal(qstore)
#else
    IF ( .NOT. gamma_only ) THEN
       DO ikq = 1, nkqs""")
    block = once(block, "    ! For US/PAW only: compute", """#endif
    ! For US/PAW only: compute""")
    exx = exx[:start] + block + exx[end:]
    # Both active CPU readers are audited. Global q/kernel/occupation indices stay.
    for begin, finish, declaration, marker in [
        ("  SUBROUTINE vexx_k(", "  END SUBROUTINE vexx_k", "    INTEGER :: ibnd, ik, im , ikq, iq, ipol", "       ikq = index_xkq(current_ik,iq)"),
        ("  FUNCTION exxenergy2_k(", "  END FUNCTION  exxenergy2_k", "                ik, ikk, ig, ikq, iq, ir", "          ikq  = index_xkq(current_ik,iq)"),
    ]:
        start = exx.index(begin)
        end = exx.index(finish, start)
        block = exx[start:end]
        block = once(block, declaration, declaration + ", iqbuf")
        indent = marker[:len(marker)-len(marker.lstrip())]
        block = once(block, marker, marker + f"\n{indent}iqbuf=ikq\n#if defined(__EXX_QSTREAM)\n{indent}CALL qs_load(qstore,ikq,exxbuff(:,:,1))\n{indent}iqbuf=1\n#endif")
        # All source-buffer reads (and excluded negrp>1 ring) use the local plane.
        block = rewrite_q_reads(block)
        exx = exx[:start] + block + exx[end:]
    edits = {path: exx}
    p = root / "PW/src/electrons.f90"
    text = p.read_text()
    text = once(text, "  IF ( restart ) THEN\n     CALL seqopn (iunres, 'restart_e', 'formatted', exst)", """#if defined(__EXX_QSTREAM)
  IF (restart .AND. xclib_dft_is('hybrid')) &
    CALL errore('electrons','qstream EXX restart import is not implemented',1)
#endif
  IF ( restart ) THEN
     CALL seqopn (iunres, 'restart_e', 'formatted', exst)""")
    text = once(text, "        IF ( .NOT. first) THEN", """        IF ( .NOT. first) THEN
#if defined(__EXX_QSTREAM)
           ! Never mislabel a single cached q plane as a full stock checkpoint.
           CALL errore('electrons','qstream EXX checkpoint export is not implemented; run unaccepted',1)
#endif""")
    edits[p] = text
    p = root / "PW/CMakeLists.txt"
    edits[p] = once(p.read_text(), "   src/exx.f90", "   src/exx_qstream.f90\n   src/exx.f90")
    p = root / "PW/src/Makefile"
    text = once(p.read_text(), "\nexx.o \\\n", "\nexx_qstream.o \\\nexx.o \\\n")
    text += "\n# Experimental private q-stream store: explicit module ordering.\nexx.o: exx_qstream.o\n"
    edits[p] = text
    for p, text in edits.items():
        p.write_text(text)
    shutil.copy2(Path(__file__).with_name("exx_qstream.f90"), root / "PW/src/exx_qstream.f90")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("private_qe_source", type=Path)
    candidate(parser.parse_args().private_qe_source)
