#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
WORK="${RUNNER_TEMP:-/tmp}/cdte-a0-runtime-readiness"
EVIDENCE="$ROOT/cdte-a0-runtime-readiness-evidence"

QE_COMMIT="500de340b820e1cb8c05f2d8bb8fced102f377c1"
ABINIT_COMMIT="d50172aacfc501b46cd33ae58fda139e674d40e3"
PSEUDO_COMMIT="7aa01a3fcf5ad226caf25bd387a9be9612be9f27"

CD_UPF_HASH="d79c48e48b2dcf1f5d347bc0b53d31b01b04acefbf7eb6f8d9f969a73a937cbd"
TE_UPF_HASH="db5bfbdcbf39096cf2a25c6382f4b07e93e25fe88a162014789466fb5fff6519"
CD_PSP8_HASH="5fe4fc81c64b1e0e912a6f362739a5d8d9cc47a26093f5e701f04c3973ced1e6"
TE_PSP8_HASH="c306f620e606a618f94f81f8283f66575b01902b7d0051fc3aa8177876c13706"

rm -rf "$WORK" "$EVIDENCE"
mkdir -p \
  "$WORK/src" \
  "$WORK/build" \
  "$WORK/runtime-pseudo" \
  "$EVIDENCE/build" \
  "$EVIDENCE/runtime" \
  "$EVIDENCE/rendered" \
  "$EVIDENCE/syntax"

exec > >(tee -a "$EVIDENCE/runtime/driver.stdout.txt") \
     2> >(tee -a "$EVIDENCE/runtime/driver.stderr.txt" >&2)

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
  g++ --version
  gfortran --version
  make --version
  cmake --version
  ninja --version
  git --version
  python --version
} > "$EVIDENCE/runtime/system.txt" 2>&1

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
clone_exact "https://github.com/abinit/abinit.git" "$ABINIT_COMMIT" "$WORK/src/abinit"
clone_exact "https://github.com/PseudoDojo/ONCVPSP-PBE-FR-PDv0.4.git" "$PSEUDO_COMMIT" "$WORK/src/pseudo"

git -C "$WORK/src/qe" submodule update --init --recursive

cat > "$EVIDENCE/runtime/source_identity.json" <<EOF
{
  "abinit": "$ABINIT_COMMIT",
  "pseudodojo": "$PSEUDO_COMMIT",
  "quantum_espresso": "$QE_COMMIT"
}
EOF

git -C "$WORK/src/qe" submodule status --recursive > "$EVIDENCE/runtime/qe_submodules.txt"
git -C "$WORK/src/abinit" submodule status --recursive > "$EVIDENCE/runtime/abinit_submodules.txt" || true

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
sha256sum "$WORK/runtime-pseudo"/* > "$EVIDENCE/runtime/runtime_pseudopotential_sha256.txt"

stage="qe_configure"
(
  cd "$WORK/src/qe"
  /usr/bin/time -v -o "$EVIDENCE/build/qe.configure.time.txt" \
    ./configure --disable-parallel --disable-openmp --enable-shared=no \
      --with-scalapack=no \
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
test -x "$PW"
test -x "$PH"

stage="abinit_prepare_generated_sources"
(
  cd "$WORK/src/abinit"
  python3 config/scripts/make-cppopts-dumper \
    > "$EVIDENCE/build/abinit.make-cppopts-dumper.out" \
    2> "$EVIDENCE/build/abinit.make-cppopts-dumper.err"
)
test -s "$WORK/src/abinit/shared/common/src/14_hidewrite/m_cppopts_dumper.F90"
sha256sum "$WORK/src/abinit/shared/common/src/14_hidewrite/m_cppopts_dumper.F90" \
  > "$EVIDENCE/build/abinit.generated-source.sha256.txt"

stage="abinit_configure"
mkdir -p "$WORK/build/abinit"
(
  export CC=gcc CXX=g++ FC=gfortran
  /usr/bin/time -v -o "$EVIDENCE/build/abinit.cmake.time.txt" \
    cmake -S "$WORK/src/abinit" -B "$WORK/build/abinit" -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
      -DBUILD_TESTING=OFF \
      > "$EVIDENCE/build/abinit.cmake.out" \
      2> "$EVIDENCE/build/abinit.cmake.err"
)
cp "$WORK/build/abinit/CMakeCache.txt" "$EVIDENCE/build/abinit.CMakeCache.txt"

stage="abinit_build"
/usr/bin/time -v -o "$EVIDENCE/build/abinit.build.time.txt" \
  cmake --build "$WORK/build/abinit" --target abinit -- -j2 \
  > "$EVIDENCE/build/abinit.build.out" \
  2> "$EVIDENCE/build/abinit.build.err"
ABINIT=$(find "$WORK/build/abinit" -type f -name abinit -perm -111 | head -n 1)
test -n "$ABINIT"
test -x "$ABINIT"

stage="executable_identity"
for executable in "$PW" "$PH" "$ABINIT"; do
  readlink -f "$executable"
  sha256sum "$executable"
  file "$executable"
done > "$EVIDENCE/runtime/executable_identity.txt"
(timeout 30 "$PW" -h || true) > "$EVIDENCE/runtime/pw.version.txt" 2>&1
(timeout 30 "$PH" -h || true) > "$EVIDENCE/runtime/ph.version.txt" 2>&1
(timeout 30 "$ABINIT" --version || true) > "$EVIDENCE/runtime/abinit.version.txt" 2>&1

test -s "$EVIDENCE/runtime/pw.version.txt"
test -s "$EVIDENCE/runtime/ph.version.txt"
test -s "$EVIDENCE/runtime/abinit.version.txt"

stage="render_inputs"
python -m tools.render_cdte_a0_runtime_inputs \
  --pseudo-dir "$WORK/runtime-pseudo" \
  --output-dir "$EVIDENCE/rendered" \
  > "$EVIDENCE/rendered/render.stdout.txt"
mkdir -p "$EVIDENCE/rendered/qe-tmp"

stage="qe_scf_nstep_zero"
/usr/bin/time -v -o "$EVIDENCE/syntax/qe-scf-dry.time.txt" \
  "$PW" -in "$EVIDENCE/rendered/inputs/cdte_qe_scf_dry.in" \
  > "$EVIDENCE/syntax/qe-scf-dry.out" \
  2> "$EVIDENCE/syntax/qe-scf-dry.err"
grep -q 'JOB DONE' "$EVIDENCE/syntax/qe-scf-dry.out"

stage="qe_ph_source_validation"
python -m tools.validate_qe_ph_input_against_source \
  --input "$EVIDENCE/rendered/inputs/cdte_qe_ph_gamma.in" \
  --definition "$WORK/src/qe/PHonon/Doc/INPUT_PH.def" \
  --output-json "$EVIDENCE/syntax/qe-ph-source-validation.json" \
  > "$EVIDENCE/syntax/qe-ph-source-validation.stdout.txt"

stage="abinit_dry_run"
(
  cd "$EVIDENCE/rendered"
  /usr/bin/time -v -o "$EVIDENCE/syntax/abinit-dry.time.txt" \
    "$ABINIT" inputs/cdte_abinit_dry.abi --dry-run \
    > "$EVIDENCE/syntax/abinit-dry.out" \
    2> "$EVIDENCE/syntax/abinit-dry.err"
)
cat "$EVIDENCE/syntax/abinit-dry.err" >> "$EVIDENCE/syntax/abinit-dry.out"

stage="summarize"
python -m tools.summarize_cdte_a0_runtime_readiness \
  --render-result "$EVIDENCE/rendered/render-result.json" \
  --ph-validation "$EVIDENCE/syntax/qe-ph-source-validation.json" \
  --qe-dry-output "$EVIDENCE/syntax/qe-scf-dry.out" \
  --abinit-dry-output "$EVIDENCE/syntax/abinit-dry.out" \
  --pw "$PW" \
  --ph "$PH" \
  --abinit "$ABINIT" \
  --pw-version "$EVIDENCE/runtime/pw.version.txt" \
  --ph-version "$EVIDENCE/runtime/ph.version.txt" \
  --abinit-version "$EVIDENCE/runtime/abinit.version.txt" \
  --source-identity "$EVIDENCE/runtime/source_identity.json" \
  --output-json "$EVIDENCE/runtime-readiness-result.json" \
  > "$EVIDENCE/runtime-readiness-result.stdout.txt"

stage="complete"
status="success"
