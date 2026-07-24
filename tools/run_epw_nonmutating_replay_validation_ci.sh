#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
WORK="${RUNNER_TEMP:-/tmp}/r02-epw-nonmutating-replay-validation"
EVIDENCE="$ROOT/r02-epw-nonmutating-replay-validation-evidence"
CONTRACT="$ROOT/first_principles/b0/r02_epw_nonmutating_replay_validation_contract.json"
BOUNDARY="$ROOT/first_principles/b0/r02_epw_replay_output_boundary_contract.json"
PATCH="$ROOT/patches/qe76-epw61-serial-epwread-epmatwp-allocation.patch"
REPLAY_INPUT="$ROOT/first_principles/b0/r02_epw_nonmutating_replay.in"

rm -rf "$WORK" "$EVIDENCE"
mkdir -p "$WORK" "$EVIDENCE"/{build,preparation/commands,replay,source,state,validated,runtime}
exec > >(tee -a "$EVIDENCE/runtime/driver.stdout.txt") \
     2> >(tee -a "$EVIDENCE/runtime/driver.stderr.txt" >&2)

status="failed"
classification="STOP_HARNESS"
stage="initialization"
build_count=0
preparation_count=0
preparation_command_count=0
replay_count=0
replay_exit_code="not_run"
material_calculation_count=0
analyzer_exit_code="not_run"

finish() {
  code=$?
  if [[ ! -f "$EVIDENCE/validated/result.json" ]]; then
    case "$stage" in
      configure_and_build) classification="STOP_BUILD" ;;
      prepare_fixture) classification="STOP_PREPARATION" ;;
      serial_replay) classification="STOP_REPLAY_RUNTIME" ;;
      *) classification="STOP_HARNESS" ;;
    esac
    python - "$EVIDENCE/validated/result.json" "$classification" "$stage" <<'PY' || true
from __future__ import annotations
import json
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(
    json.dumps(
        {
            "schema_version": "1.0",
            "stage": "B0_epw_nonmutating_replay_validation_result",
            "program": "R02",
            "issue": 371,
            "status": "stop",
            "classification": sys.argv[2],
            "last_stage": sys.argv[3],
            "analysis_completed": False,
            "exporter_enabled": False,
            "material_calculation_count": 0,
            "automatic_successor_authorized": False,
        },
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)
PY
  fi
  python - "$EVIDENCE" "$status" "$classification" "$stage" "$code" \
    "$build_count" "$preparation_count" "$preparation_command_count" \
    "$replay_count" "$replay_exit_code" "$material_calculation_count" \
    "$analyzer_exit_code" <<'PY' || true
from __future__ import annotations
import json
from pathlib import Path
import sys

evidence = Path(sys.argv[1])
payload = {
    "schema_version": "1.0",
    "stage": "B0_epw_nonmutating_replay_validation_runtime_status",
    "issue": 371,
    "status": sys.argv[2],
    "classification": sys.argv[3],
    "last_stage": sys.argv[4],
    "driver_exit_code": int(sys.argv[5]),
    "build_count": int(sys.argv[6]),
    "preparation_count": int(sys.argv[7]),
    "preparation_command_count": int(sys.argv[8]),
    "replay_count": int(sys.argv[9]),
    "replay_exit_code": (
        sys.argv[10] if sys.argv[10] == "not_run" else int(sys.argv[10])
    ),
    "material_calculation_count": int(sys.argv[11]),
    "analyzer_exit_code": (
        sys.argv[12] if sys.argv[12] == "not_run" else int(sys.argv[12])
    ),
}
(evidence / "runtime" / "status.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
PY
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
} > "$EVIDENCE/runtime/system.txt" 2>&1

stage="contract_gate"
python - <<'PY'
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess

execution_path = Path("first_principles/b0/r02_epw_nonmutating_replay_validation_contract.json")
boundary_path = Path("first_principles/b0/r02_epw_replay_output_boundary_contract.json")
execution = json.loads(execution_path.read_text())
boundary = json.loads(boundary_path.read_text())
assert execution["stage"] == "B0_epw_nonmutating_replay_validation"
assert execution["issue"] == 371
assert execution["design_issue"] == 355
assert execution["design_merge_commit"] == "4cb0b9fef65a67e56a794fd3676ef2e687d0e1c3"
assert execution["phase"] == "one_pinned_execution"
assert boundary["stage"] == "B0_epw_replay_output_boundary_design"
assert boundary["issue"] == 355 and boundary["phase"] == "design_only"
assert boundary["historical_issue_350_result_unchanged"] is True
patch = Path(execution["patch"]["path"])
assert hashlib.sha256(patch.read_bytes()).hexdigest() == execution["patch"]["sha256"]
replay = Path(execution["fixture"]["replay_input_path"])
assert hashlib.sha256(replay.read_bytes()).hexdigest() == execution["fixture"]["replay_input_sha256"]
assert subprocess.check_output(["git", "hash-object", str(boundary_path)], text=True).strip() == execution["boundary_design"]["contract_git_blob_sha"]
assert subprocess.check_output(["git", "hash-object", str(replay)], text=True).strip() == execution["fixture"]["replay_input_git_blob_sha"]
auth = execution["authorization"]
for key in (
    "source_clone_and_verify",
    "apply_exact_patch",
    "exactly_one_build",
    "exactly_one_preparation",
    "exactly_one_serial_replay",
    "repository_analysis",
):
    assert auth[key] is True
for key in (
    "automatic_retry",
    "patch_adjustment_after_execution",
    "enabled_exporter_replay",
    "second_disabled_replay",
    "mpi_execution",
    "soc_fixture",
    "cdte_hgte_or_alloy_calculation",
    "a1_a2_a3",
    "parameter_sweep",
    "automatic_successor",
):
    assert auth[key] is False
assert execution["fixture"]["exporter_enabled"] is False
assert execution["fixture"]["soc_enabled"] is False
PY
cp "$CONTRACT" "$EVIDENCE/source/execution-contract.json"
cp "$BOUNDARY" "$EVIDENCE/source/boundary-contract.json"
cp "$PATCH" "$EVIDENCE/source/allocation.patch"
cp "$REPLAY_INPUT" "$EVIDENCE/source/replay.in"

stage="focused_tests"
python -m pytest -vv \
  tests/test_r02_epw_nonmutating_replay_validation.py \
  tests/test_r02_epw_replay_output_boundary_design.py \
  tests/test_r02_epw_replay_output_boundary_source_audit.py \
  tests/test_r02_epw_serial_epmatwp_diagnosis.py \
  2>&1 | tee "$EVIDENCE/validated/focused-pytest.txt"
bash -n tools/run_epw_nonmutating_replay_validation_ci.sh

stage="source_clone_and_verify"
SOURCE_COMMIT=$(python - <<'PY'
import json
from pathlib import Path
print(json.loads(Path("first_principles/b0/r02_epw_nonmutating_replay_validation_contract.json").read_text())["source"]["commit_sha"])
PY
)
SOURCE_URL=$(python - <<'PY'
import json
from pathlib import Path
print(json.loads(Path("first_principles/b0/r02_epw_nonmutating_replay_validation_contract.json").read_text())["source"]["clone_url"])
PY
)
git init -q "$WORK/qe"
git -C "$WORK/qe" remote add origin "$SOURCE_URL"
git -C "$WORK/qe" fetch --depth 1 origin "$SOURCE_COMMIT"
git -C "$WORK/qe" checkout --detach -q FETCH_HEAD
git -C "$WORK/qe" submodule update --init --recursive --depth 1
test "$(git -C "$WORK/qe" rev-parse HEAD)" = "$SOURCE_COMMIT"
git -C "$WORK/qe" show -s --format=fuller HEAD > "$EVIDENCE/source/commit-metadata.txt"
python - "$WORK/qe" "$CONTRACT" <<'PY' > r02-epw-nonmutating-replay-validation-evidence/source/verified-source-files.json
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1])
contract = json.loads(Path(sys.argv[2]).read_text())
records = []
for relative, expected in contract["source"]["required_files_sha256"].items():
    path = repo / relative
    if not path.is_file():
        raise SystemExit(f"missing pinned source file: {relative}")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != expected:
        raise SystemExit(f"SHA-256 mismatch for {relative}: {digest}")
    records.append({"path": relative, "sha256": digest, "size_bytes": path.stat().st_size})
io_blob = subprocess.check_output(
    ["git", "-C", str(repo), "hash-object", "EPW/src/io/io.f90"], text=True
).strip()
if io_blob != contract["source"]["io_f90_git_blob_sha"]:
    raise SystemExit(f"io.f90 Git blob mismatch: {io_blob}")
print(json.dumps({"io_f90_git_blob_sha": io_blob, "files": records}, indent=2, sort_keys=True))
PY
(
  cd "$WORK/qe"
  git archive --format=tar HEAD | sha256sum
) > "$EVIDENCE/source/source-tree-archive-sha256.txt"
test "$(cut -d' ' -f1 "$EVIDENCE/source/source-tree-archive-sha256.txt")" = \
  "$(python - <<'PY'
import json
from pathlib import Path
print(json.loads(Path('first_principles/b0/r02_epw_nonmutating_replay_validation_contract.json').read_text())['source']['source_tree_archive_sha256'])
PY
)"

stage="apply_exact_patch"
git -C "$WORK/qe" apply --check "$PATCH"
git -C "$WORK/qe" apply "$PATCH"
git -C "$WORK/qe" diff --check
git -C "$WORK/qe" diff -- EPW/src/io/io.f90 > "$EVIDENCE/source/applied.patch"
python - "$WORK/qe/EPW/src/io/io.f90" <<'PY' > r02-epw-nonmutating-replay-validation-evidence/source/patched-source-check.json
from __future__ import annotations
import json
from pathlib import Path
import sys

text = Path(sys.argv[1]).read_text()
start = text.index("SUBROUTINE epw_read(")
end = text.index("END SUBROUTINE epw_read", start)
body = text[start:end]
allocation = "ALLOCATE(epmatwp(nbndsub, nbndsub, nrr_k, nmodes, nirg_loc), STAT = ierr)"
count = body.count(allocation)
preprocessor = body.index("#if defined(__MPI)", body.index("IF (etf_mem == 0) THEN"))
allocation_position = body.index(allocation, body.index("IF (etf_mem == 0) THEN"))
if count != 1 or allocation_position >= preprocessor:
    raise SystemExit("patched allocation is not exactly once above MPI split")
print(json.dumps({"allocation_count": count, "allocation_before_mpi_split": True}, indent=2))
PY

stage="configure_and_build"
build_count=1
cd "$WORK/qe"
./configure --disable-parallel --enable-openmp \
  2>&1 | tee "$EVIDENCE/build/configure.txt"
make -j2 pw ph epw \
  2>&1 | tee "$EVIDENCE/build/make.txt"
for executable in bin/pw.x bin/ph.x bin/epw.x; do
  test -x "$executable"
  sha256sum "$executable" >> "$EVIDENCE/build/executable-sha256.txt"
done

run_command() {
  local number="$1"
  local identifier="$2"
  local executable="$3"
  local stdin_path="$4"
  shift 4
  local stdout="$EVIDENCE/preparation/commands/$number-$identifier.stdout.txt"
  local stderr="$EVIDENCE/preparation/commands/$number-$identifier.stderr.txt"
  local exit_file="$EVIDENCE/preparation/commands/$number-$identifier.exit-code.txt"
  local code=0
  : > "$stdout"
  : > "$stderr"
  if [[ "$stdin_path" == "-" ]]; then
    if (cd "$PREP_DIR" && "$executable" "$@") >> "$stdout" 2>> "$stderr"; then
      code=0
    else
      code=$?
    fi
  else
    if (cd "$PREP_DIR" && "$executable" "$@" < "$stdin_path") >> "$stdout" 2>> "$stderr"; then
      code=0
    else
      code=$?
    fi
  fi
  printf '%s\n' "$code" > "$exit_file"
  preparation_command_count=$((preparation_command_count + 1))
  if (( code != 0 )); then
    return "$code"
  fi
}

stage="prepare_fixture"
PREP_DIR="$WORK/qe/test-suite/r02_nonmutating_preparation"
cp -a "$WORK/qe/test-suite/epw_base" "$PREP_DIR"
PW_X="$WORK/qe/bin/pw.x"
PH_X="$WORK/qe/bin/ph.x"
EPW_X="$WORK/qe/bin/epw.x"
PYTHON_X="$(command -v python3)"
EPW_BIN="$WORK/qe/EPW/bin"
preparation_count=1
run_command 01 pw-scf "$PW_X" - -input scf.in
run_command 02 ph "$PH_X" - -input ph.in
run_command 03 pp "$PYTHON_X" pp.in "$EPW_BIN/pp.py"
run_command 04 pw-scf-epw "$PW_X" - -input scf_epw.in
run_command 05 pw-nscf-epw "$PW_X" - -input nscf_epw.in
run_command 06 epw "$EPW_X" - -input epw1.in
test "$preparation_command_count" -eq 6

stage="project_immutable_seed"
export PYTHONPATH="$ROOT"
REPLAY_DIR="$WORK/qe/test-suite/r02_nonmutating_replay"
python - "$PREP_DIR" "$REPLAY_DIR" "$BOUNDARY" "$EVIDENCE/state" <<'PY'
from __future__ import annotations
import json
from pathlib import Path
import shutil
import sys

from tools.design_epw_replay_output_boundary import (
    build_tree_manifest,
    manifest_payload,
    project_immutable_seed,
    write_json,
)

preparation = Path(sys.argv[1])
replay = Path(sys.argv[2])
contract = json.loads(Path(sys.argv[3]).read_text())
evidence = Path(sys.argv[4])
complete = build_tree_manifest(preparation)
projection = project_immutable_seed(complete, contract)
seed = projection["seed"]
write_json(manifest_payload(complete), evidence / "preparation-complete.json")
write_json(manifest_payload(seed), evidence / "seed.json")
write_json({"removed": projection["removed"]}, evidence / "seed-projection.json")
if replay.exists():
    raise SystemExit("replay directory already exists")
replay.mkdir(parents=True)
for record in seed:
    source = preparation / record.relative_path
    destination = replay / record.relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
replay_manifest = build_tree_manifest(replay)
write_json(manifest_payload(replay_manifest), evidence / "replay-pre.json")
if [record.as_dict() for record in replay_manifest] != [record.as_dict() for record in seed]:
    raise SystemExit("projected replay seed is not byte-identical")
PY

stage="serial_replay"
unset R02_EXPORT_RAW_VERTEX R02_EXPORT_IK_GLOBAL R02_RAW_VERTEX_PATH || true
for name in R02_EXPORT_RAW_VERTEX R02_EXPORT_IK_GLOBAL R02_RAW_VERTEX_PATH; do
  if [[ -v "$name" ]]; then
    echo "exporter variable unexpectedly set: $name" >&2
    exit 1
  fi
done
printf '%s\n' "exporter variables unset" > "$EVIDENCE/replay/export-environment.txt"
: > "$EVIDENCE/replay/stdout.txt"
: > "$EVIDENCE/replay/stderr.txt"
replay_count=1
set +e
(
  cd "$REPLAY_DIR"
  "$EPW_X" -input "$REPLAY_INPUT"
) >> "$EVIDENCE/replay/stdout.txt" 2>> "$EVIDENCE/replay/stderr.txt"
replay_exit_code=$?
set -e
printf '%s\n' "$replay_exit_code" > "$EVIDENCE/replay/exit-code.txt"

stage="post_replay_analysis"
python - "$REPLAY_DIR" "$EVIDENCE/state/replay-post.json" <<'PY'
from pathlib import Path
import sys
from tools.design_epw_replay_output_boundary import build_tree_manifest, manifest_payload, write_json
write_json(manifest_payload(build_tree_manifest(Path(sys.argv[1]))), Path(sys.argv[2]))
PY
set +e
python -m tools.analyze_epw_nonmutating_replay_validation \
  --execution-contract "$CONTRACT" \
  --boundary-contract "$BOUNDARY" \
  --seed-manifest "$EVIDENCE/state/seed.json" \
  --post-manifest "$EVIDENCE/state/replay-post.json" \
  --replay-dir "$REPLAY_DIR" \
  --stdout "$EVIDENCE/replay/stdout.txt" \
  --stderr "$EVIDENCE/replay/stderr.txt" \
  --exit-code "$replay_exit_code" \
  --output "$EVIDENCE/validated/result.json"
analyzer_exit_code=$?
set -e
classification=$(python - "$EVIDENCE/validated/result.json" <<'PY'
import json
from pathlib import Path
import sys
print(json.loads(Path(sys.argv[1]).read_text())['classification'])
PY
)

stage="evidence_volume"
EVIDENCE_BYTES=$(du -sb "$EVIDENCE" | cut -f1)
MAX_BYTES=$(python - "$CONTRACT" <<'PY'
import json
from pathlib import Path
import sys
print(json.loads(Path(sys.argv[1]).read_text())['resource_limits']['maximum_evidence_bytes'])
PY
)
if (( EVIDENCE_BYTES > MAX_BYTES )); then
  echo "evidence exceeds ceiling: $EVIDENCE_BYTES > $MAX_BYTES" >&2
  exit 1
fi
printf '%s\n' "$EVIDENCE_BYTES" > "$EVIDENCE/runtime/evidence-size-bytes.txt"

if (( analyzer_exit_code != 0 )); then
  exit "$analyzer_exit_code"
fi

stage="complete"
status="passed"
classification="PASS_NONMUTATING_SERIAL_REPLAY"
