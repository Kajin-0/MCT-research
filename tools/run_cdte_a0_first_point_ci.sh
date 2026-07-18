#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
WORK="${RUNNER_TEMP:-/tmp}/cdte-a0-first-point"
EVIDENCE="$ROOT/cdte-a0-first-point-evidence"

QE_COMMIT="500de340b820e1cb8c05f2d8bb8fced102f377c1"
PSEUDO_COMMIT="7aa01a3fcf5ad226caf25bd387a9be9612be9f27"
CD_UPF_HASH="d79c48e48b2dcf1f5d347bc0b53d31b01b04acefbf7eb6f8d9f969a73a937cbd"
TE_UPF_HASH="db5bfbdcbf39096cf2a25c6382f4b07e93e25fe88a162014789466fb5fff6519"
CD_PSP8_HASH="5fe4fc81c64b1e0e912a6f362739a5d8d9cc47a26093f5e701f04c3973ced1e6"
TE_PSP8_HASH="c306f620e606a618f94f81f8283f66575b01902b7d0051fc3aa8177876c13706"

rm -rf "$WORK" "$EVIDENCE"
mkdir -p \
  "$WORK/src" \
  "$WORK/runtime-pseudo" \
  "$EVIDENCE/build" \
  "$EVIDENCE/runtime" \
  "$EVIDENCE/rendered" \
  "$EVIDENCE/raw" \
  "$EVIDENCE/validated"

exec > >(tee -a "$EVIDENCE/runtime/driver.stdout.txt") \
     2> >(tee -a "$EVIDENCE/runtime/driver.stderr.txt" >&2)

status="failed"
stage="initialization"
calculation_executed="false"
phonon_executed="false"
finish() {
  code=$?
  {
    printf 'status=%s\n' "$status"
    printf 'last_stage=%s\n' "$stage"
    printf 'exit_code=%s\n' "$code"
    printf 'calculation_executed=%s\n' "$calculation_executed"
    printf 'phonon_executed=%s\n' "$phonon_executed"
    date -u '+finished_utc=%Y-%m-%dT%H:%M:%SZ'
  } > "$EVIDENCE/status.txt"
  find "$EVIDENCE" -type f ! -name evidence_sha256.txt -print0 \
    | sort -z | xargs -0 sha256sum > "$EVIDENCE/evidence_sha256.txt" || true
  exit "$code"
}
trap finish EXIT

stage="system_manifest"
{
  date -u '+started_utc=%Y-%m-%dT%H:%M:%SZ'
  uname -a
  lscpu
  free -h
  df -h
  ulimit -a
  gcc --version
  gfortran --version
  make --version
  git --version
  python --version
} > "$EVIDENCE/runtime/system.txt" 2>&1

stage="repository_readiness"
python "$ROOT/tools/check_cdte_a0_readiness.py" \
  --require-ready \
  --report-json "$EVIDENCE/validated/repository-readiness.json" \
  > "$EVIDENCE/validated/repository-readiness.stdout.txt"

python - <<'PY' > "$EVIDENCE/validated/first-point-contract-check.json"
import json
from pathlib import Path

contract = json.loads(Path("first_principles/a0/cdte_a0_first_point_contract.json").read_text())
auth = contract["authorization"]
assert contract["stage"] == "A0_first_point_breadth_smoke"
assert auth["one_qe_scf_point"] is True
assert auth["one_gamma_phonon_dielectric_born_point"] is True
assert auth["convergence_claim"] is False
assert auth["automatic_ladder_continuation"] is False
assert auth["a1_electron_phonon"] is False
assert auth["production_ahc"] is False
assert auth["hgte"] is False
assert auth["alloy"] is False
print(json.dumps({"passed": True, "stage": contract["stage"]}, indent=2))
PY

clone_exact() {
  local url=$1 commit=$2 destination=$3
  git init -q "$destination"
  git -C "$destination" remote add origin "$url"
  git -C "$destination" fetch --depth 1 origin "$commit"
  git -C "$destination" checkout --detach -q FETCH_HEAD
  test "$(git -C "$destination" rev-parse HEAD)" = "$commit"
}

stage="source_acquisition"
clone_exact "https://gitlab.com/QEF/q-e.git" "$QE_COMMIT" "$WORK/src/qe"
clone_exact "https://github.com/PseudoDojo/ONCVPSP-PBE-FR-PDv0.4.git" "$PSEUDO_COMMIT" "$WORK/src/pseudo"
git -C "$WORK/src/qe" submodule update --init --recursive

cat > "$EVIDENCE/runtime/source_identity.json" <<EOF
{
  "quantum_espresso": "$QE_COMMIT",
  "pseudodojo": "$PSEUDO_COMMIT"
}
EOF
git -C "$WORK/src/qe" submodule status --recursive \
  > "$EVIDENCE/runtime/qe_submodules.txt"

stage="pseudopotential_staging"
git -C "$WORK/src/pseudo" show "$PSEUDO_COMMIT:Cd/Cd-sp_r.upf" \
  > "$WORK/runtime-pseudo/Cd-sp_r.upf"
git -C "$WORK/src/pseudo" show "$PSEUDO_COMMIT:Te/Te-d_r.upf" \
  > "$WORK/runtime-pseudo/Te-d_r.upf"
git -C "$WORK/src/pseudo" show "$PSEUDO_COMMIT:Cd/Cd-sp_r.psp8" \
  > "$WORK/runtime-pseudo/Cd-sp_r.psp8"
git -C "$WORK/src/pseudo" show "$PSEUDO_COMMIT:Te/Te-d_r.psp8" \
  > "$WORK/runtime-pseudo/Te-d_r.psp8"

printf '%s  %s\n' \
  "$CD_UPF_HASH" "$WORK/runtime-pseudo/Cd-sp_r.upf" \
  "$TE_UPF_HASH" "$WORK/runtime-pseudo/Te-d_r.upf" \
  "$CD_PSP8_HASH" "$WORK/runtime-pseudo/Cd-sp_r.psp8" \
  "$TE_PSP8_HASH" "$WORK/runtime-pseudo/Te-d_r.psp8" \
  | tee "$EVIDENCE/runtime/expected_pseudopotential_sha256.txt" \
  | sha256sum -c -
sha256sum "$WORK/runtime-pseudo"/* \
  > "$EVIDENCE/runtime/runtime_pseudopotential_sha256.txt"

stage="qe_configure"
(
  cd "$WORK/src/qe"
  /usr/bin/time -v -o "$EVIDENCE/build/qe.configure.time.txt" \
    ./configure --disable-parallel --enable-openmp --with-scalapack=no \
      > "$EVIDENCE/build/qe.configure.out" \
      2> "$EVIDENCE/build/qe.configure.err"
)
cp "$WORK/src/qe/install/configure.msg" "$EVIDENCE/build/qe.configure.msg" || true
cp "$WORK/src/qe/install/config.log" "$EVIDENCE/build/qe.config.log" || true
cp "$WORK/src/qe/make.inc" "$EVIDENCE/build/qe.make.inc" || true

stage="qe_build"
/usr/bin/time -v -o "$EVIDENCE/build/qe.make.time.txt" \
  make -C "$WORK/src/qe" -j2 pw ph \
  > "$EVIDENCE/build/qe.make.out" \
  2> "$EVIDENCE/build/qe.make.err"
PW="$WORK/src/qe/bin/pw.x"
PH="$WORK/src/qe/bin/ph.x"
DYNMAT="$WORK/src/qe/bin/dynmat.x"
test -x "$PW"
test -x "$PH"
test -x "$DYNMAT"

stage="executable_identity"
for executable in "$PW" "$PH" "$DYNMAT"; do
  readlink -f "$executable"
  sha256sum "$executable"
  file "$executable"
done > "$EVIDENCE/runtime/executable_identity.txt"
(timeout 30 "$PW" -h || true) > "$EVIDENCE/runtime/pw.version.txt" 2>&1
(timeout 30 "$PH" -h || true) > "$EVIDENCE/runtime/ph.version.txt" 2>&1
(timeout 30 "$DYNMAT" -h || true) > "$EVIDENCE/runtime/dynmat.version.txt" 2>&1

stage="render_inputs"
python -m tools.render_cdte_a0_first_point \
  --pseudo-dir "$WORK/runtime-pseudo" \
  --output-dir "$EVIDENCE/rendered" \
  > "$EVIDENCE/rendered/render.stdout.txt"
mkdir -p "$EVIDENCE/rendered/qe-tmp"
sha256sum "$EVIDENCE/rendered/inputs"/* \
  > "$EVIDENCE/runtime/rendered_input_sha256.txt"

export OMP_NUM_THREADS=2
export OMP_STACKSIZE=1G
export OPENBLAS_NUM_THREADS=1

stage="scf"
calculation_executed="true"
/usr/bin/time -v -o "$EVIDENCE/raw/scf.time.txt" \
  "$PW" -in "$EVIDENCE/rendered/inputs/cdte_qe_scf_first_point.in" \
  > "$EVIDENCE/raw/scf.out" \
  2> "$EVIDENCE/raw/scf.err"
grep -q 'convergence has been achieved' "$EVIDENCE/raw/scf.out"
grep -q 'JOB DONE' "$EVIDENCE/raw/scf.out"
! grep -qiE 'Error in routine|NaN|SIGSEGV|stopping' "$EVIDENCE/raw/scf.out"

SCHEMA="$EVIDENCE/rendered/qe-tmp/cdte_a0_first.save/data-file-schema.xml"
test -s "$SCHEMA"
cp "$SCHEMA" "$EVIDENCE/raw/data-file-schema.xml"

stage="eigenvalue_extraction"
python "$ROOT/tools/extract_qe_ks_energies.py" \
  "$SCHEMA" \
  --output-json "$EVIDENCE/raw/qe-exact-eigenvalues.json" \
  > "$EVIDENCE/raw/qe-exact-eigenvalues.stdout.txt"
python - "$EVIDENCE/raw/qe-exact-eigenvalues.json" \
  > "$EVIDENCE/validated/gamma-eigenvalues.json" <<'PY'
import json, math, pathlib, sys

source = json.loads(pathlib.Path(sys.argv[1]).read_text())
blocks = source["blocks"]
gamma = [
    block for block in blocks
    if math.sqrt(sum(float(x) ** 2 for x in block["k_point_crystal"])) < 1e-12
]
if len(gamma) != 1:
    raise SystemExit(f"expected one Gamma block, found {len(gamma)}")
block = gamma[0]
if len(block["eigenvalues_ev"]) != 40:
    raise SystemExit("expected 40 Gamma eigenvalues")
print(json.dumps({
    "status": "raw_gamma_eigenvalues_not_irrep_assignment_not_converged",
    "k_point_index": block["index"],
    "k_point_crystal": block["k_point_crystal"],
    "weight": block["weight"],
    "num_bands": len(block["eigenvalues_ev"]),
    "eigenvalues_ev": block["eigenvalues_ev"],
    "occupations": block["occupations"],
}, indent=2, sort_keys=True))
PY

stage="gamma_phonon"
phonon_executed="true"
/usr/bin/time -v -o "$EVIDENCE/raw/ph.time.txt" \
  "$PH" -in "$EVIDENCE/rendered/inputs/cdte_qe_ph_gamma_first_point.in" \
  > "$EVIDENCE/raw/ph.out" \
  2> "$EVIDENCE/raw/ph.err"
grep -q 'JOB DONE' "$EVIDENCE/raw/ph.out"
! grep -qiE 'Error in routine|NaN|SIGSEGV|stopping' "$EVIDENCE/raw/ph.out"
DYN="$EVIDENCE/rendered/cdte_a0_first.gamma.dyn"
test -s "$DYN"
cp "$DYN" "$EVIDENCE/raw/cdte_a0_first.gamma.dyn"

stage="dynmat_no_asr"
cat > "$EVIDENCE/rendered/inputs/cdte_qe_dynmat_no_asr.in" <<EOF
&INPUT
  fildyn = '$DYN'
  asr = 'no'
  filout = '$EVIDENCE/raw/dynmat-no-asr.modes'
/
EOF
/usr/bin/time -v -o "$EVIDENCE/raw/dynmat-no-asr.time.txt" \
  "$DYNMAT" -in "$EVIDENCE/rendered/inputs/cdte_qe_dynmat_no_asr.in" \
  > "$EVIDENCE/raw/dynmat-no-asr.out" \
  2> "$EVIDENCE/raw/dynmat-no-asr.err"
grep -q 'JOB DONE' "$EVIDENCE/raw/dynmat-no-asr.out"

stage="dynmat_simple_asr"
cat > "$EVIDENCE/rendered/inputs/cdte_qe_dynmat_simple_asr.in" <<EOF
&INPUT
  fildyn = '$DYN'
  asr = 'simple'
  filout = '$EVIDENCE/raw/dynmat-simple-asr.modes'
/
EOF
/usr/bin/time -v -o "$EVIDENCE/raw/dynmat-simple-asr.time.txt" \
  "$DYNMAT" -in "$EVIDENCE/rendered/inputs/cdte_qe_dynmat_simple_asr.in" \
  > "$EVIDENCE/raw/dynmat-simple-asr.out" \
  2> "$EVIDENCE/raw/dynmat-simple-asr.err"
grep -q 'JOB DONE' "$EVIDENCE/raw/dynmat-simple-asr.out"

stage="calculation_state"
python - <<'PY' > "$EVIDENCE/validated/calculation-state.json"
import json
print(json.dumps({
    "schema_version": "1.0",
    "stage": "A0_first_point_breadth_smoke",
    "status": "raw_first_point_completed_pending_scientific_audit",
    "scf_executed": True,
    "scf_converged": True,
    "gamma_eigenvalues_preserved": True,
    "gamma_phonon_executed": True,
    "dielectric_and_born_requested": True,
    "dynmat_no_asr_completed": True,
    "dynmat_simple_asr_completed": True,
    "scientific_result_validated": False,
    "convergence_claim": False,
    "automatic_next_point_authorized": False,
    "a1_or_production_authorized": False,
}, indent=2, sort_keys=True))
PY

stage="output_manifest"
{
  du -sh "$EVIDENCE/rendered/qe-tmp" || true
  du -sh "$EVIDENCE/raw" || true
  wc -l "$EVIDENCE/raw"/*.out || true
  df -h
  free -h
} > "$EVIDENCE/runtime/output_sizes_and_resources.txt"
sha256sum "$EVIDENCE/raw"/* > "$EVIDENCE/runtime/raw_output_sha256.txt"

status="success"
stage="complete"
