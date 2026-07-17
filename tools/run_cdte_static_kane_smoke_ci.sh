#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
WORK="${RUNNER_TEMP:-/tmp}/cdte-kane-runtime"
EVIDENCE="$ROOT/cdte-kane-evidence"
INPUTS="$ROOT/first_principles/a0/cdte_static_kane_smoke_inputs"

QE_COMMIT="500de340b820e1cb8c05f2d8bb8fced102f377c1"
W90_COMMIT="1d6b187374a2d50b509e5e79e2cab01a79ff7ce1"
PSEUDO_COMMIT="7aa01a3fcf5ad226caf25bd387a9be9612be9f27"
CD_HASH="d79c48e48b2dcf1f5d347bc0b53d31b01b04acefbf7eb6f8d9f969a73a937cbd"
TE_HASH="db5bfbdcbf39096cf2a25c6382f4b07e93e25fe88a162014789466fb5fff6519"

rm -rf "$WORK" "$EVIDENCE"
mkdir -p "$WORK/src" "$WORK/run/pseudo" "$WORK/run/tmp" "$EVIDENCE/build" "$EVIDENCE/runtime" "$EVIDENCE/raw"

status="failed"
stage="initialization"
finish() {
  code=$?
  {
    printf 'status=%s\n' "$status"
    printf 'last_stage=%s\n' "$stage"
    printf 'exit_code=%s\n' "$code"
    date -u '+finished_utc=%Y-%m-%dT%H:%M:%SZ'
  } > "$EVIDENCE/status.txt"
  find "$EVIDENCE" -type f -print0 | sort -z | xargs -0 sha256sum > "$EVIDENCE/evidence_sha256.txt" || true
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
  cmake --version
  git --version
  python --version
} > "$EVIDENCE/runtime/system.txt" 2>&1

stage="source_acquisition"
clone_exact() {
  local url=$1 commit=$2 destination=$3
  git init -q "$destination"
  git -C "$destination" remote add origin "$url"
  git -C "$destination" fetch --depth 1 origin "$commit"
  git -C "$destination" checkout --detach -q FETCH_HEAD
  test "$(git -C "$destination" rev-parse HEAD)" = "$commit"
}

clone_exact "https://gitlab.com/QEF/q-e.git" "$QE_COMMIT" "$WORK/src/qe"
clone_exact "https://github.com/wannier-developers/wannier90.git" "$W90_COMMIT" "$WORK/src/wannier90"
clone_exact "https://github.com/PseudoDojo/ONCVPSP-PBE-FR-PDv0.4.git" "$PSEUDO_COMMIT" "$WORK/src/pseudo"

git -C "$WORK/src/qe" submodule update --init --recursive

{
  printf 'qe_repository=%s\n' 'https://gitlab.com/QEF/q-e.git'
  printf 'qe_commit=%s\n' "$(git -C "$WORK/src/qe" rev-parse HEAD)"
  printf 'wannier90_repository=%s\n' 'https://github.com/wannier-developers/wannier90.git'
  printf 'wannier90_commit=%s\n' "$(git -C "$WORK/src/wannier90" rev-parse HEAD)"
  printf 'pseudodojo_repository=%s\n' 'https://github.com/PseudoDojo/ONCVPSP-PBE-FR-PDv0.4.git'
  printf 'pseudodojo_commit=%s\n' "$(git -C "$WORK/src/pseudo" rev-parse HEAD)"
} > "$EVIDENCE/runtime/source_identity.txt"
git -C "$WORK/src/qe" submodule status --recursive > "$EVIDENCE/runtime/qe_submodules.txt"

stage="pseudopotential_verification"
cp "$WORK/src/pseudo/Cd/Cd-sp_r.upf" "$WORK/run/pseudo/Cd-sp_r.upf"
cp "$WORK/src/pseudo/Te/Te-d_r.upf" "$WORK/run/pseudo/Te-d_r.upf"
actual_cd=$(sha256sum "$WORK/run/pseudo/Cd-sp_r.upf" | awk '{print $1}')
actual_te=$(sha256sum "$WORK/run/pseudo/Te-d_r.upf" | awk '{print $1}')
printf '%s  Cd-sp_r.upf\n%s  Te-d_r.upf\n' "$actual_cd" "$actual_te" > "$EVIDENCE/runtime/pseudopotential_sha256.txt"
test "$actual_cd" = "$CD_HASH"
test "$actual_te" = "$TE_HASH"

stage="wannier90_build"
cp "$WORK/src/wannier90/config/make.inc.gfort" "$WORK/src/wannier90/make.inc"
/usr/bin/time -v -o "$EVIDENCE/build/wannier90.time.txt" \
  make -C "$WORK/src/wannier90" wannier > "$EVIDENCE/build/wannier90.make.out" 2> "$EVIDENCE/build/wannier90.make.err"
W90="$WORK/src/wannier90/wannier90.x"
test -x "$W90"

stage="qe_configure"
mkdir -p "$WORK/src/qe/build"
(
  cd "$WORK/src/qe/build"
  /usr/bin/time -v -o "$EVIDENCE/build/qe.configure.time.txt" \
    ../configure --disable-parallel --enable-openmp --with-scalapack=no \
    > "$EVIDENCE/build/qe.configure.out" 2> "$EVIDENCE/build/qe.configure.err"
)
cp "$WORK/src/qe/build/configure.msg" "$EVIDENCE/build/qe.configure.msg" || true
cp "$WORK/src/qe/build/config.log" "$EVIDENCE/build/qe.config.log" || true
cp "$WORK/src/qe/build/make.inc" "$EVIDENCE/build/qe.make.inc" || true

stage="qe_build"
/usr/bin/time -v -o "$EVIDENCE/build/qe.make.time.txt" \
  make -C "$WORK/src/qe/build" -j2 pw pp > "$EVIDENCE/build/qe.make.out" 2> "$EVIDENCE/build/qe.make.err"
PW="$WORK/src/qe/build/bin/pw.x"
PW2WAN="$WORK/src/qe/build/bin/pw2wannier90.x"
test -x "$PW"
test -x "$PW2WAN"

stage="executable_identity"
for executable in "$PW" "$PW2WAN" "$W90"; do
  readlink -f "$executable"
  sha256sum "$executable"
  file "$executable"
done > "$EVIDENCE/runtime/executable_identity.txt"
(timeout 20 "$PW" -h || true) > "$EVIDENCE/runtime/pw.help.txt" 2>&1
(timeout 20 "$PW2WAN" -h || true) > "$EVIDENCE/runtime/pw2wannier90.help.txt" 2>&1
(timeout 20 "$W90" -v || true) > "$EVIDENCE/runtime/wannier90.version.txt" 2>&1

stage="stage_inputs"
cp "$INPUTS"/cdte_kane.* "$WORK/run/"
(
  cd "$WORK/run"
  sha256sum cdte_kane.scf.in cdte_kane.nscf.in cdte_kane.win cdte_kane.pw2wan.in \
    > "$EVIDENCE/runtime/input_sha256.txt"
)

stage="wannier90_preprocess"
(
  cd "$WORK/run"
  /usr/bin/time -v -o "$EVIDENCE/raw/wannier90_pp.time.txt" \
    "$W90" -pp cdte_kane > "$EVIDENCE/raw/wannier90_pp.out" 2> "$EVIDENCE/raw/wannier90_pp.err"
)
test -s "$WORK/run/cdte_kane.nnkp"
cp "$WORK/run/cdte_kane.nnkp" "$EVIDENCE/raw/"
sha256sum "$WORK/run/cdte_kane.win" "$WORK/run/cdte_kane.nnkp" > "$EVIDENCE/runtime/wannier90_preprocess_sha256.txt"
python - "$WORK/run/cdte_kane.nnkp" <<'PY' > "$EVIDENCE/runtime/nnkp_validation.json"
import json, pathlib, sys
text = pathlib.Path(sys.argv[1]).read_text()
start = text.lower().index('begin nnkpts')
end = text.lower().index('end nnkpts', start)
rows = [line.split() for line in text[start:].splitlines()[1:] if line.strip()][:13]
expected = [[str(i), '1', '0', '0', '0'] for i in range(1, 14)]
if rows != expected:
    raise SystemExit(f'nnkpts mismatch: {rows!r}')
print(json.dumps({'status':'exact_gamma_star_verified','row_count':len(rows),'rows':rows}, indent=2))
PY

export OMP_NUM_THREADS=2
export OMP_STACKSIZE=1G
export OPENBLAS_NUM_THREADS=1

stage="scf"
(
  cd "$WORK/run"
  /usr/bin/time -v -o "$EVIDENCE/raw/scf.time.txt" \
    "$PW" -in cdte_kane.scf.in > "$EVIDENCE/raw/scf.out" 2> "$EVIDENCE/raw/scf.err"
)
grep -q 'JOB DONE' "$EVIDENCE/raw/scf.out"

stage="nscf"
(
  cd "$WORK/run"
  /usr/bin/time -v -o "$EVIDENCE/raw/nscf.time.txt" \
    "$PW" -in cdte_kane.nscf.in > "$EVIDENCE/raw/nscf.out" 2> "$EVIDENCE/raw/nscf.err"
)
grep -q 'JOB DONE' "$EVIDENCE/raw/nscf.out"

stage="overlap_export"
(
  cd "$WORK/run"
  /usr/bin/time -v -o "$EVIDENCE/raw/pw2wannier90.time.txt" \
    "$PW2WAN" -in cdte_kane.pw2wan.in > "$EVIDENCE/raw/pw2wannier90.out" 2> "$EVIDENCE/raw/pw2wannier90.err"
)
test -s "$WORK/run/cdte_kane.mmn"
cp "$WORK/run/cdte_kane.mmn" "$EVIDENCE/raw/"
sha256sum "$WORK/run/cdte_kane.mmn" > "$EVIDENCE/runtime/mmn_sha256.txt"
python "$ROOT/tools/check_wannier90_gamma_star_mmn.py" \
  "$WORK/run/cdte_kane.mmn" --expected-bands 40 \
  --summary-json "$EVIDENCE/runtime/mmn_validation.json" \
  > "$EVIDENCE/runtime/mmn_validation.stdout.txt"

stage="output_manifest"
{
  du -sh "$WORK/run/tmp" || true
  du -sh "$WORK/run/cdte_kane.mmn" || true
  wc -l "$EVIDENCE/raw"/*.out "$EVIDENCE/raw/cdte_kane.mmn" || true
} > "$EVIDENCE/runtime/output_sizes.txt"
sha256sum "$EVIDENCE/raw"/* > "$EVIDENCE/runtime/raw_output_sha256.txt"

status="success"
stage="complete"
