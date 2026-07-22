#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
WORK="${RUNNER_TEMP:-/tmp}/cdte-a0-zeu-zue"
EVIDENCE="$ROOT/cdte-a0-zeu-zue-evidence"
QE_COMMIT="500de340b820e1cb8c05f2d8bb8fced102f377c1"
PSEUDO_COMMIT="7aa01a3fcf5ad226caf25bd387a9be9612be9f27"
CD_UPF_HASH="d79c48e48b2dcf1f5d347bc0b53d31b01b04acefbf7eb6f8d9f969a73a937cbd"
TE_UPF_HASH="db5bfbdcbf39096cf2a25c6382f4b07e93e25fe88a162014789466fb5fff6519"
CD_PSP8_HASH="5fe4fc81c64b1e0e912a6f362739a5d8d9cc47a26093f5e701f04c3973ced1e6"
TE_PSP8_HASH="c306f620e606a618f94f81f8283f66575b01902b7d0051fc3aa8177876c13706"

rm -rf "$WORK" "$EVIDENCE"
mkdir -p "$WORK/src" "$WORK/runtime-pseudo" \
  "$EVIDENCE/build" "$EVIDENCE/runtime" "$EVIDENCE/rendered" \
  "$EVIDENCE/raw" "$EVIDENCE/validated"
exec > >(tee -a "$EVIDENCE/runtime/driver.stdout.txt") \
     2> >(tee -a "$EVIDENCE/runtime/driver.stderr.txt" >&2)

status="failed"
stage="initialization"
scf_execution_count=0
response_route_count=0
finish() {
  code=$?
  {
    printf 'status=%s\n' "$status"
    printf 'last_stage=%s\n' "$stage"
    printf 'exit_code=%s\n' "$code"
    printf 'scf_execution_count=%s\n' "$scf_execution_count"
    printf 'response_route_count=%s\n' "$response_route_count"
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
  gcc --version
  gfortran --version
  make --version
  git --version
  python --version
} > "$EVIDENCE/runtime/system.txt" 2>&1

stage="repository_readiness"
python "$ROOT/tools/check_cdte_a0_readiness.py" --require-ready \
  --report-json "$EVIDENCE/validated/repository-readiness.json" \
  > "$EVIDENCE/validated/repository-readiness.stdout.txt"
python - <<'PY' > "$EVIDENCE/validated/diagnostic-contract-check.json"
import json
from pathlib import Path
contract = json.loads(Path("first_principles/a0/cdte_a0_zeu_zue_contract.json").read_text())
assert contract["stage"] == "A0_same_state_zeu_zue_response_diagnostic"
assert contract["issue"] == 271
assert contract["required_settings"]["ecutrho_ry"] == 570.0
assert contract["required_settings"]["ph_tr2"] == 1e-14
assert contract["routes"]["zeu"]["zeu"] is True
assert contract["routes"]["zeu"]["zue"] is False
assert contract["routes"]["zue"]["zeu"] is False
assert contract["routes"]["zue"]["zue"] is True
assert contract["authorization"]["automatic_retry"] is False
assert contract["authorization"]["automatic_ladder_continuation"] is False
assert contract["authorization"]["a1_electron_phonon"] is False
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
printf '{"quantum_espresso":"%s","pseudodojo":"%s"}\n' \
  "$QE_COMMIT" "$PSEUDO_COMMIT" > "$EVIDENCE/runtime/source_identity.json"
git -C "$WORK/src/qe" submodule status --recursive > "$EVIDENCE/runtime/qe_submodules.txt"

stage="pseudopotential_staging"
git -C "$WORK/src/pseudo" show "$PSEUDO_COMMIT:Cd/Cd-sp_r.upf" > "$WORK/runtime-pseudo/Cd-sp_r.upf"
git -C "$WORK/src/pseudo" show "$PSEUDO_COMMIT:Te/Te-d_r.upf" > "$WORK/runtime-pseudo/Te-d_r.upf"
git -C "$WORK/src/pseudo" show "$PSEUDO_COMMIT:Cd/Cd-sp_r.psp8" > "$WORK/runtime-pseudo/Cd-sp_r.psp8"
git -C "$WORK/src/pseudo" show "$PSEUDO_COMMIT:Te/Te-d_r.psp8" > "$WORK/runtime-pseudo/Te-d_r.psp8"
printf '%s  %s\n' \
  "$CD_UPF_HASH" "$WORK/runtime-pseudo/Cd-sp_r.upf" \
  "$TE_UPF_HASH" "$WORK/runtime-pseudo/Te-d_r.upf" \
  "$CD_PSP8_HASH" "$WORK/runtime-pseudo/Cd-sp_r.psp8" \
  "$TE_PSP8_HASH" "$WORK/runtime-pseudo/Te-d_r.psp8" \
  | tee "$EVIDENCE/runtime/expected_pseudopotential_sha256.txt" | sha256sum -c -
sha256sum "$WORK/runtime-pseudo"/* > "$EVIDENCE/runtime/runtime_pseudopotential_sha256.txt"

stage="qe_build"
(
  cd "$WORK/src/qe"
  /usr/bin/time -v -o "$EVIDENCE/build/qe.configure.time.txt" \
    ./configure --disable-parallel --enable-openmp --with-scalapack=no \
    > "$EVIDENCE/build/qe.configure.out" 2> "$EVIDENCE/build/qe.configure.err"
)
/usr/bin/time -v -o "$EVIDENCE/build/qe.make.time.txt" \
  make -C "$WORK/src/qe" -j2 pw ph \
  > "$EVIDENCE/build/qe.make.out" 2> "$EVIDENCE/build/qe.make.err"
PW="$WORK/src/qe/bin/pw.x"
PH="$WORK/src/qe/bin/ph.x"
for executable in "$PW" "$PH"; do test -x "$executable"; done
for executable in "$PW" "$PH"; do sha256sum "$executable"; done \
  > "$EVIDENCE/runtime/executable_identity.txt"

stage="render_inputs"
python -m tools.render_cdte_a0_stricter_response \
  --pseudo-dir "$WORK/runtime-pseudo" --output-dir "$EVIDENCE/rendered/base" \
  > "$EVIDENCE/rendered/render.stdout.txt"
mkdir -p "$EVIDENCE/rendered/base/qe-tmp" "$EVIDENCE/rendered/inputs"
python - <<'PY_INPUTS'
import json
from pathlib import Path

root = Path("cdte-a0-zeu-zue-evidence")
contract = json.loads(Path("first_principles/a0/cdte_a0_zeu_zue_contract.json").read_text())
reference = json.loads(Path("first_principles/a0/cdte_a0_stricter_response_reference_result.json").read_text())
rendered = json.loads((root / "rendered/base/render-result.json").read_text())
for name in (
    "reference_lattice_angstrom", "ecutwfc_ry", "ecutrho_ry", "k_grid",
    "k_grid_shift", "nbnd", "scf_conv_thr_ry", "ph_tr2",
):
    assert contract["required_settings"][name] == reference["settings"][name]
for name in (
    "reference_lattice_angstrom", "ecutwfc_ry", "ecutrho_ry", "k_grid",
    "k_grid_shift", "nbnd", "scf_conv_thr_ry", "ph_tr2",
):
    assert rendered["settings"][name] == reference["settings"][name]
assert rendered["settings"]["q_point"] == [0.0, 0.0, 0.0]
assert contract["baseline_run_spec"] == {"ecutrho_ry": 456.0, "ph_tr2": 1e-10}
base_ph = (root / "rendered/base/inputs/cdte_qe_ph_gamma_stricter_response.in").read_text()
for route, flags in contract["routes"].items():
    text = base_ph
    old_outdir = str((root / "rendered/base/qe-tmp").resolve())
    new_outdir = str((root / f"rendered/qe-{route}").resolve())
    text = text.replace(f"outdir = '{old_outdir}'", f"outdir = '{new_outdir}'")
    old_dyn = str((root / "rendered/base/cdte_a0_strict.gamma.dyn").resolve())
    new_dyn = str((root / f"rendered/cdte_a0_{route}.gamma.dyn").resolve())
    text = text.replace(f"fildyn = '{old_dyn}'", f"fildyn = '{new_dyn}'")
    explicit = (
        f"  zeu = {'.true.' if flags['zeu'] else '.false.'}\n"
        f"  zue = {'.true.' if flags['zue'] else '.false.'}\n"
    )
    text = text.replace("/\n0.0 0.0 0.0", explicit + "/\n0.0 0.0 0.0")
    output = root / f"rendered/inputs/cdte_qe_ph_gamma_{route}.in"
    output.write_text(text)
scf = root / "rendered/base/inputs/cdte_qe_scf_stricter_response.in"
(root / "rendered/inputs/cdte_qe_scf_zeu_zue.in").write_text(scf.read_text())
PY_INPUTS
sha256sum "$EVIDENCE/rendered/inputs"/* > "$EVIDENCE/runtime/rendered_input_sha256.txt"
export OMP_NUM_THREADS=2 OMP_STACKSIZE=1G OPENBLAS_NUM_THREADS=1

stage="scf"
scf_execution_count=1
/usr/bin/time -v -o "$EVIDENCE/raw/scf.time.txt" \
  "$PW" -in "$EVIDENCE/rendered/inputs/cdte_qe_scf_zeu_zue.in" \
  > "$EVIDENCE/raw/scf.out" 2> "$EVIDENCE/raw/scf.err"
grep -qi 'convergence has been achieved' "$EVIDENCE/raw/scf.out"
grep -q 'JOB DONE' "$EVIDENCE/raw/scf.out"
! grep -qiE 'Error in routine|NaN|SIGSEGV|stopping' "$EVIDENCE/raw/scf.out"
SCHEMA="$EVIDENCE/rendered/base/qe-tmp/cdte_a0_strict.save/data-file-schema.xml"
test -s "$SCHEMA"
cp "$SCHEMA" "$EVIDENCE/raw/data-file-schema.xml"

stage="eigenvalue_extraction"
python "$ROOT/tools/extract_qe_ks_energies.py" "$SCHEMA" \
  --output-json "$EVIDENCE/raw/qe-exact-eigenvalues.json" \
  > "$EVIDENCE/raw/qe-exact-eigenvalues.stdout.txt"

hash_save_tree() {
  local root=$1 output=$2
  (
    cd "$root"
    find . -type f -print0 | sort -z | xargs -0 sha256sum
  ) > "$output"
}

stage="same_state_fanout"
SAVE_NAME="cdte_a0_strict.save"
hash_save_tree "$EVIDENCE/rendered/base/qe-tmp/$SAVE_NAME" "$EVIDENCE/runtime/base_save_tree_sha256.txt"
cp -a "$EVIDENCE/rendered/base/qe-tmp" "$EVIDENCE/rendered/qe-zeu"
cp -a "$EVIDENCE/rendered/base/qe-tmp" "$EVIDENCE/rendered/qe-zue"
hash_save_tree "$EVIDENCE/rendered/qe-zeu/$SAVE_NAME" "$EVIDENCE/runtime/zeu_save_tree_sha256.txt"
hash_save_tree "$EVIDENCE/rendered/qe-zue/$SAVE_NAME" "$EVIDENCE/runtime/zue_save_tree_sha256.txt"
cmp "$EVIDENCE/runtime/base_save_tree_sha256.txt" "$EVIDENCE/runtime/zeu_save_tree_sha256.txt"
cmp "$EVIDENCE/runtime/base_save_tree_sha256.txt" "$EVIDENCE/runtime/zue_save_tree_sha256.txt"

stage="zeu_response"
response_route_count=1
/usr/bin/time -v -o "$EVIDENCE/raw/ph-zeu.time.txt" \
  "$PH" -in "$EVIDENCE/rendered/inputs/cdte_qe_ph_gamma_zeu.in" \
  > "$EVIDENCE/raw/ph-zeu.out" 2> "$EVIDENCE/raw/ph-zeu.err"
grep -q 'JOB DONE' "$EVIDENCE/raw/ph-zeu.out"
grep -q 'Effective charges (d Force / dE)' "$EVIDENCE/raw/ph-zeu.out"
! grep -qiE 'Error in routine|NaN|SIGSEGV|stopping' "$EVIDENCE/raw/ph-zeu.out"

after_zeu="$EVIDENCE/rendered/qe-zeu/$SAVE_NAME"
test -d "$after_zeu"

stage="zue_response"
response_route_count=2
/usr/bin/time -v -o "$EVIDENCE/raw/ph-zue.time.txt" \
  "$PH" -in "$EVIDENCE/rendered/inputs/cdte_qe_ph_gamma_zue.in" \
  > "$EVIDENCE/raw/ph-zue.out" 2> "$EVIDENCE/raw/ph-zue.err"
grep -q 'JOB DONE' "$EVIDENCE/raw/ph-zue.out"
grep -q 'Effective charges (d P / du)' "$EVIDENCE/raw/ph-zue.out"
! grep -qiE 'Error in routine|NaN|SIGSEGV|stopping' "$EVIDENCE/raw/ph-zue.out"

stage="same_state_manifest"
python - <<'PY' > "$EVIDENCE/validated/same-state-manifest.json"
import json
from pathlib import Path

root = Path("cdte-a0-zeu-zue-evidence")
base = (root / "runtime/base_save_tree_sha256.txt").read_text()
zeu = (root / "runtime/zeu_save_tree_sha256.txt").read_text()
zue = (root / "runtime/zue_save_tree_sha256.txt").read_text()
zeu_input = (root / "rendered/inputs/cdte_qe_ph_gamma_zeu.in").read_text()
zue_input = (root / "rendered/inputs/cdte_qe_ph_gamma_zue.in").read_text()
route_settings_match = all((
    "zeu = .true." in zeu_input,
    "zue = .false." in zeu_input,
    "zeu = .false." in zue_input,
    "zue = .true." in zue_input,
    "ecutrho = 570.0" in (root / "rendered/inputs/cdte_qe_scf_zeu_zue.in").read_text(),
))
print(json.dumps({
    "schema_version": "1.0",
    "scf_execution_count": 1,
    "response_route_count": 2,
    "base_and_zeu_save_match": base == zeu,
    "base_and_zue_save_match": base == zue,
    "route_settings_match_contract": route_settings_match,
    "automatic_retry_performed": False,
    "parameter_sweep_performed": False,
    "a1_or_production_executed": False,
}, indent=2, sort_keys=True))
PY

stage="scientific_audit"
python "$ROOT/tools/analyze_cdte_a0_zeu_zue.py" \
  --scf "$EVIDENCE/raw/scf.out" \
  --zeu "$EVIDENCE/raw/ph-zeu.out" \
  --zue "$EVIDENCE/raw/ph-zue.out" \
  --eigenvalues "$EVIDENCE/raw/qe-exact-eigenvalues.json" \
  --state-manifest "$EVIDENCE/validated/same-state-manifest.json" \
  --contract "$ROOT/first_principles/a0/cdte_a0_zeu_zue_contract.json" \
  --output-json "$EVIDENCE/validated/zeu-zue-diagnostic-result.json" \
  > "$EVIDENCE/validated/zeu-zue-diagnostic-result.stdout.txt"

stage="claim_boundary_check"
python - <<'PY' > "$EVIDENCE/validated/claim-boundary-check.json"
import json
from pathlib import Path
result = json.loads(Path("cdte-a0-zeu-zue-evidence/validated/zeu-zue-diagnostic-result.json").read_text())
assert result["decision"]["a1_electron_phonon_authorized"] is False
assert result["decision"]["automatic_followup_authorized"] is False
assert result["authorization"]["production_ahc"] is False
assert result["authorization"]["dense_epw"] is False
assert result["authorization"]["hgte"] is False
assert result["authorization"]["alloy"] is False
print(json.dumps({"passed": True, "action": result["decision"]["action"]}, indent=2))
PY

stage="output_manifest"
sha256sum "$EVIDENCE/raw"/* > "$EVIDENCE/runtime/raw_output_sha256.txt"
{
  du -sh "$EVIDENCE/rendered/base/qe-tmp" "$EVIDENCE/rendered/qe-zeu" \
    "$EVIDENCE/rendered/qe-zue" "$EVIDENCE/raw" || true
  wc -l "$EVIDENCE/raw"/*.out || true
  df -h
  free -h
} > "$EVIDENCE/runtime/output_sizes_and_resources.txt"
status="success"
stage="complete"
