#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
WORK="${RUNNER_TEMP:-/tmp}/r02-epw-same-state"
EVIDENCE="$ROOT/r02-epw-same-state-evidence"
CONTRACT="$ROOT/first_principles/b0/r02_epw_same_state_execution_contract.json"
DESIGN_CONTRACT="$ROOT/first_principles/b0/r02_epw_same_state_attribution_contract.json"
REPLAY_INPUT="$ROOT/first_principles/b0/r02_epw_same_state_replay.in"
PATCH="$ROOT/patches/qe76-epw61-r02-raw-vertex-export.patch"

rm -rf "$WORK" "$EVIDENCE"
mkdir -p "$WORK" "$EVIDENCE"/{build,preparation/commands,replays,raw,source,state,validated,runtime}
for replay in disabled_a disabled_b enabled; do
  mkdir -p "$EVIDENCE/replays/$replay"
done

exec > >(tee -a "$EVIDENCE/runtime/driver.stdout.txt") \
     2> >(tee -a "$EVIDENCE/runtime/driver.stderr.txt" >&2)

status="failed"
stage="initialization"
build_count=0
preparation_command_count=0
replay_count=0
material_calculation_count=0
finish() {
  code=$?
  {
    printf 'status=%s\n' "$status"
    printf 'last_stage=%s\n' "$stage"
    printf 'exit_code=%s\n' "$code"
    printf 'build_count=%s\n' "$build_count"
    printf 'preparation_command_count=%s\n' "$preparation_command_count"
    printf 'replay_count=%s\n' "$replay_count"
    printf 'material_calculation_count=%s\n' "$material_calculation_count"
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
  git --version
  gcc --version | head -n 1
  gfortran --version | head -n 1
  make --version | head -n 1
  python --version
  ldconfig -p | grep -E 'blas|lapack|fftw' | head -n 30 || true
} > "$EVIDENCE/runtime/system.txt" 2>&1

stage="contract_gate"
python - <<'PY'
import hashlib
import json
from pathlib import Path

execution = json.loads(
    Path("first_principles/b0/r02_epw_same_state_execution_contract.json").read_text()
)
design = json.loads(
    Path("first_principles/b0/r02_epw_same_state_attribution_contract.json").read_text()
)
assert execution["stage"] == "B0_epw_same_state_attribution_execution"
assert execution["issue"] == 332
assert execution["phase"] == "one_pinned_execution"
assert execution["design_merge_commit"] == "cb4b13c36bca8d1b47080be23a2c7190b35c6f1a"
assert design["stage"] == "B0_epw_same_state_attribution_design"
assert design["issue"] == 318 and design["phase"] == "design_only"
assert execution["replay"]["input_sha256"] == design["replay_input"]["sha256"]
assert hashlib.sha256(
    Path(execution["replay"]["input_path"]).read_bytes()
).hexdigest() == execution["replay"]["input_sha256"]
assert hashlib.sha256(
    Path(execution["observational_patch"]["path"]).read_bytes()
).hexdigest() == execution["observational_patch"]["sha256"]
auth = execution["authorization"]
for field in (
    "source_clone_and_verify",
    "observational_patch_application",
    "exactly_one_pinned_build",
    "exactly_one_preparation_sequence",
    "exactly_three_final_replays",
    "repository_analysis",
):
    assert auth[field] is True
for field in (
    "automatic_retry",
    "fourth_replay",
    "alternate_build",
    "parameter_sweep",
    "output_removal_or_manifest_relaxation",
    "threshold_fitting",
    "soc_fixture",
    "cdte_hgte_or_alloy_calculation",
    "a1_a2_a3",
    "automatic_phase_transition",
):
    assert auth[field] is False
assert execution["preparation"]["command_count"] == 6
assert execution["replay"]["replay_count"] == 3
assert execution["prepared_state"]["preparation_outputs_may_not_be_removed_before_manifest"] is True
PY
cp "$CONTRACT" "$EVIDENCE/source/execution-contract.json"
cp "$DESIGN_CONTRACT" "$EVIDENCE/source/design-contract.json"
cp "$REPLAY_INPUT" "$EVIDENCE/source/replay-input.in"

stage="focused_tests"
python -m pytest -vv \
  tests/test_r02_epw_same_state_execution.py \
  tests/test_r02_epw_raw_vertex_analyzer.py \
  tests/test_r02_epw_same_state_attribution_design.py \
  tests/test_r02_epw_same_state_source_identities.py \
  2>&1 | tee "$EVIDENCE/validated/focused-pytest.txt"

stage="source_clone_and_verify"
SOURCE_COMMIT=$(python - <<'PY'
import json
from pathlib import Path
print(json.loads(Path("first_principles/b0/r02_epw_same_state_execution_contract.json").read_text())["source"]["commit_sha"])
PY
)
SOURCE_URL=$(python - <<'PY'
import json
from pathlib import Path
print(json.loads(Path("first_principles/b0/r02_epw_same_state_execution_contract.json").read_text())["source"]["clone_url"])
PY
)
git init -q "$WORK/qe"
git -C "$WORK/qe" remote add origin "$SOURCE_URL"
git -C "$WORK/qe" fetch --depth 1 origin "$SOURCE_COMMIT"
git -C "$WORK/qe" checkout --detach -q FETCH_HEAD
git -C "$WORK/qe" submodule update --init --recursive --depth 1
test "$(git -C "$WORK/qe" rev-parse HEAD)" = "$SOURCE_COMMIT"
git -C "$WORK/qe" show -s --format=fuller HEAD > "$EVIDENCE/source/commit-metadata.txt"

python - "$WORK/qe" "$CONTRACT" <<'PY' > "$EVIDENCE/source/verified-sha256-manifest.json"
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys

repo = Path(sys.argv[1])
contract = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
records = []
for relative, expected in contract["source"]["required_sha256"].items():
    path = repo / relative
    if not path.is_file():
        raise SystemExit(f"missing pinned source file: {relative}")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != expected:
        raise SystemExit(f"SHA-256 mismatch for {relative}: {digest}")
    records.append({"path": relative, "sha256": digest, "size_bytes": path.stat().st_size})
print(json.dumps({"source_commit": contract["source"]["commit_sha"], "files": records}, indent=2, sort_keys=True))
PY

python - "$CONTRACT" <<'PY' > "$WORK/git-blob-expectations.tsv"
import json
from pathlib import Path
import sys
contract = json.loads(Path(sys.argv[1]).read_text())
for path, blob in contract["source"]["required_git_blob_ids"].items():
    print(f"{path}\t{blob}")
PY
: > "$EVIDENCE/source/verified-git-blob-manifest.tsv"
while IFS=$'\t' read -r relative expected; do
  observed=$(git -C "$WORK/qe" hash-object "$relative")
  test "$observed" = "$expected"
  printf '%s\t%s\n' "$relative" "$observed" >> "$EVIDENCE/source/verified-git-blob-manifest.tsv"
done < "$WORK/git-blob-expectations.tsv"

test "$(git -C "$WORK/qe" hash-object test-suite/run-epw.sh)" = \
  "$(python - <<'PY'
import json
from pathlib import Path
print(json.loads(Path('first_principles/b0/r02_epw_same_state_execution_contract.json').read_text())['source']['run_epw_git_blob_sha'])
PY
)"
(
  cd "$WORK/qe"
  git archive --format=tar HEAD | sha256sum
) > "$EVIDENCE/source/source-tree-archive-sha256.txt"
test "$(cut -d' ' -f1 "$EVIDENCE/source/source-tree-archive-sha256.txt")" = \
  "$(python - <<'PY'
import json
from pathlib import Path
print(json.loads(Path('first_principles/b0/r02_epw_same_state_execution_contract.json').read_text())['source']['source_tree_archive_sha256'])
PY
)"

stage="apply_observational_patch"
git -C "$WORK/qe" apply --check "$PATCH"
git -C "$WORK/qe" apply "$PATCH"
git -C "$WORK/qe" diff --check
git -C "$WORK/qe" diff -- EPW/src/selfen.f90 > "$EVIDENCE/source/applied-observational.patch"
sha256sum "$PATCH" "$EVIDENCE/source/applied-observational.patch" \
  > "$EVIDENCE/source/patch-sha256.txt"

stage="configure_and_build"
build_count=1
cd "$WORK/qe"
./configure --disable-parallel --enable-openmp \
  2>&1 | tee "$EVIDENCE/build/configure.txt"
make -j2 pw ph epw \
  2>&1 | tee "$EVIDENCE/build/make.txt"
test "$build_count" -eq 1
for executable in bin/pw.x bin/ph.x bin/epw.x; do
  test -x "$executable"
  sha256sum "$executable" >> "$EVIDENCE/build/executable-sha256.txt"
done
ldd bin/epw.x > "$EVIDENCE/build/epw-ldd.txt" || true

PW_X="$WORK/qe/bin/pw.x"
PH_X="$WORK/qe/bin/ph.x"
EPW_X="$WORK/qe/bin/epw.x"
EPW_BIN="$WORK/qe/EPW/bin"
PYTHON_X="$(command -v python3)"
PREPARATION_STATE="$WORK/qe/test-suite/r02_same_state_preparation"
cp -a "$WORK/qe/test-suite/epw_base" "$PREPARATION_STATE"

run_preparation_command() {
  local number="$1"
  local identifier="$2"
  local executable="$3"
  local stdin_name="$4"
  shift 4
  local stdout="$EVIDENCE/preparation/commands/$number-$identifier.stdout.txt"
  local stderr="$EVIDENCE/preparation/commands/$number-$identifier.stderr.txt"
  local exit_code_path="$EVIDENCE/preparation/commands/$number-$identifier.exit-code.txt"
  local process_code=0
  printf '# R02 same-state preparation command=%s\n' "$identifier" > "$stdout"
  printf '# R02 same-state preparation command=%s\n' "$identifier" > "$stderr"
  if [[ "$stdin_name" == "-" ]]; then
    if (cd "$PREPARATION_STATE" && "$executable" "$@") >> "$stdout" 2>> "$stderr"; then
      process_code=0
    else
      process_code=$?
    fi
  else
    if (cd "$PREPARATION_STATE" && "$executable" "$@" < "$stdin_name") \
      >> "$stdout" 2>> "$stderr"; then
      process_code=0
    else
      process_code=$?
    fi
  fi
  preparation_command_count=$((preparation_command_count + 1))
  printf '%s\n' "$process_code" > "$exit_code_path"
  test -s "$stdout"
  test -s "$stderr"
  test -s "$exit_code_path"
  if (( process_code != 0 )); then
    return "$process_code"
  fi
}

stage="one_preparation_sequence"
unset R02_EXPORT_RAW_VERTEX R02_EXPORT_IK_GLOBAL R02_RAW_VERTEX_PATH || true
run_preparation_command 01 pw-scf "$PW_X" - -input scf.in
run_preparation_command 02 ph "$PH_X" - -input ph.in
run_preparation_command 03 pp "$PYTHON_X" pp.in "$EPW_BIN/pp.py"
run_preparation_command 04 pw-scf-epw "$PW_X" - -input scf_epw.in
run_preparation_command 05 pw-nscf-epw "$PW_X" - -input nscf_epw.in
run_preparation_command 06 epw "$EPW_X" - -input epw1.in
test "$preparation_command_count" -eq 6
find "$PREPARATION_STATE" -type f -printf '%P %s\n' | sort \
  > "$EVIDENCE/state/preparation-generated-files.txt"

stage="freeze_complete_prepared_state"
export PYTHONPATH="$ROOT"
python - "$PREPARATION_STATE" "$CONTRACT" "$EVIDENCE/state/prepared-manifest.json" <<'PY'
from pathlib import Path
import json
import sys
from tools.design_epw_same_state_attribution import (
    build_tree_manifest,
    manifest_payload,
    require_paths,
    write_json,
)
root = Path(sys.argv[1])
contract = json.loads(Path(sys.argv[2]).read_text())
entries = build_tree_manifest(root)
require_paths(entries, contract["prepared_state"]["required_paths"])
write_json(manifest_payload(entries), Path(sys.argv[3]))
PY

CLONE_ROOT="$WORK/replay-clones"
mkdir -p "$CLONE_ROOT"
for replay in disabled_a disabled_b enabled; do
  cp -a "$PREPARATION_STATE" "$CLONE_ROOT/$replay"
done

python - "$CLONE_ROOT" "$CONTRACT" "$EVIDENCE/state" <<'PY'
from pathlib import Path
import json
import sys
from tools.design_epw_same_state_attribution import (
    assert_identical_manifests,
    build_tree_manifest,
    manifest_payload,
    require_paths,
    write_json,
)
root = Path(sys.argv[1])
contract = json.loads(Path(sys.argv[2]).read_text())
out = Path(sys.argv[3])
clone_ids = contract["replay"]["clone_ids"]
manifests = {}
for clone_id in clone_ids:
    entries = build_tree_manifest(root / clone_id)
    require_paths(entries, contract["prepared_state"]["required_paths"])
    manifests[clone_id] = entries
    write_json(manifest_payload(entries), out / f"{clone_id}.pre-manifest.json")
assert_identical_manifests(manifests, clone_ids)
write_json(
    {
        "schema_version": "1.0",
        "pre_manifests_identical": True,
        "required_paths_present": True,
        "clone_ids": clone_ids,
        "manifest_sha256": manifest_payload(manifests[clone_ids[0]])["manifest_sha256"],
    },
    out / "pre-replay-gate.json",
)
PY

run_replay() {
  local replay="$1"
  local state_dir="$CLONE_ROOT/$replay"
  local stdout="$EVIDENCE/replays/$replay/epw.stdout.txt"
  local stderr="$EVIDENCE/replays/$replay/epw.stderr.txt"
  local exit_code_path="$EVIDENCE/replays/$replay/epw.exit-code.txt"
  local process_code=0
  printf '# R02 same-state replay=%s\n' "$replay" > "$stdout"
  printf '# R02 same-state replay=%s\n' "$replay" > "$stderr"
  if [[ "$replay" == "enabled" ]]; then
    export R02_EXPORT_RAW_VERTEX=1
    export R02_EXPORT_IK_GLOBAL=1
    export R02_RAW_VERTEX_PATH="$EVIDENCE/raw/epw-raw-vertex.txt"
  else
    unset R02_EXPORT_RAW_VERTEX R02_EXPORT_IK_GLOBAL R02_RAW_VERTEX_PATH || true
  fi
  if (cd "$state_dir" && "$EPW_X" -input "$REPLAY_INPUT") >> "$stdout" 2>> "$stderr"; then
    process_code=0
  else
    process_code=$?
  fi
  replay_count=$((replay_count + 1))
  printf '%s\n' "$process_code" > "$exit_code_path"
  test -s "$stdout"
  test -s "$stderr"
  test -s "$exit_code_path"
  find "$state_dir" -type f -printf '%P %s\n' | sort \
    > "$EVIDENCE/replays/$replay/generated-files.txt"
  if (( process_code != 0 )); then
    return "$process_code"
  fi
}

stage="three_final_epw_replays"
rm -f "$EVIDENCE/raw/epw-raw-vertex.txt"
run_replay disabled_a
run_replay disabled_b
run_replay enabled
test "$replay_count" -eq 3
test -s "$EVIDENCE/raw/epw-raw-vertex.txt"

stage="post_replay_state_integrity"
python - "$CLONE_ROOT" "$CONTRACT" "$EVIDENCE/state" <<'PY'
from pathlib import Path
import json
import sys
from tools.design_epw_same_state_attribution import (
    build_tree_manifest,
    compare_pre_post_manifests,
    manifest_payload,
    write_json,
)
root = Path(sys.argv[1])
contract = json.loads(Path(sys.argv[2]).read_text())
out = Path(sys.argv[3])
clone_ids = contract["replay"]["clone_ids"]
allowed = contract["prepared_state"]["allowed_new_file_patterns"]
comparisons = {}
for clone_id in clone_ids:
    pre_payload = json.loads((out / f"{clone_id}.pre-manifest.json").read_text())
    from tools.design_epw_same_state_attribution import TreeEntry
    pre_entries = [TreeEntry(**record) for record in pre_payload["files"]]
    post_entries = build_tree_manifest(root / clone_id)
    write_json(manifest_payload(post_entries), out / f"{clone_id}.post-manifest.json")
    comparisons[clone_id] = compare_pre_post_manifests(pre_entries, post_entries, allowed)
pre_gate = json.loads((out / "pre-replay-gate.json").read_text())
write_json(
    {
        "schema_version": "1.0",
        "stage": "B0_epw_same_state_integrity",
        "pre_manifests_identical": pre_gate["pre_manifests_identical"],
        "required_paths_present": pre_gate["required_paths_present"],
        "prepared_manifest_sha256": pre_gate["manifest_sha256"],
        "replay_comparisons": comparisons,
    },
    out / "state-integrity.json",
)
PY

stage="preservation_gate"
PREP_STREAMS=$(find "$EVIDENCE/preparation/commands" -type f \
  \( -name '*.stdout.txt' -o -name '*.stderr.txt' \) | wc -l)
test "$PREP_STREAMS" -eq 12
REPLAY_STREAMS=$(find "$EVIDENCE/replays" -type f \
  \( -name '*.stdout.txt' -o -name '*.stderr.txt' \) | wc -l)
test "$REPLAY_STREAMS" -eq 6
EXIT_FILES=$(find "$EVIDENCE/preparation/commands" "$EVIDENCE/replays" \
  -type f -name '*.exit-code.txt' | wc -l)
test "$EXIT_FILES" -eq 9
if find "$EVIDENCE/preparation/commands" "$EVIDENCE/replays" \
  -type f -name '*.exit-code.txt' -exec grep -L '^0$' {} + | grep -q .; then
  echo "one or more fixed commands returned nonzero" >&2
  exit 1
fi
printf '%s\n' "$PREP_STREAMS" > "$EVIDENCE/runtime/preparation-stream-count.txt"
printf '%s\n' "$REPLAY_STREAMS" > "$EVIDENCE/runtime/replay-stream-count.txt"
printf '%s\n' "$EXIT_FILES" > "$EVIDENCE/runtime/exit-code-file-count.txt"

stage="terminal_analysis"
cd "$ROOT"
python -m tools.analyze_epw_same_state_attribution \
  --raw "$EVIDENCE/raw/epw-raw-vertex.txt" \
  --disabled-a-stdout "$EVIDENCE/replays/disabled_a/epw.stdout.txt" \
  --disabled-b-stdout "$EVIDENCE/replays/disabled_b/epw.stdout.txt" \
  --enabled-stdout "$EVIDENCE/replays/enabled/epw.stdout.txt" \
  --state-integrity "$EVIDENCE/state/state-integrity.json" \
  --contract "$CONTRACT" \
  --output-json "$EVIDENCE/validated/terminal-result.json"
test -s "$EVIDENCE/validated/terminal-result.json"

stage="evidence_volume"
EVIDENCE_BYTES=$(du -sb "$EVIDENCE" | cut -f1)
MAX_BYTES=$(python - <<'PY'
import json
from pathlib import Path
print(json.loads(Path('first_principles/b0/r02_epw_same_state_execution_contract.json').read_text())['thresholds']['maximum_evidence_bytes'])
PY
)
if (( EVIDENCE_BYTES > MAX_BYTES )); then
  echo "evidence exceeds declared ceiling: $EVIDENCE_BYTES > $MAX_BYTES" >&2
  exit 1
fi
printf '%s\n' "$EVIDENCE_BYTES" > "$EVIDENCE/runtime/evidence-size-bytes.txt"

stage="complete"
status="completed"
