#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
WORK="${RUNNER_TEMP:-/tmp}/r02-epw-direct-fixture"
EVIDENCE="$ROOT/r02-epw-direct-fixture-evidence"
EXECUTION_CONTRACT="$ROOT/first_principles/b0/r02_epw_direct_fixture_execution_contract.json"
ANALYSIS_CONTRACT="$ROOT/first_principles/b0/r02_epw_raw_vertex_fixture_contract.json"
DESIGN_CONTRACT="$ROOT/first_principles/b0/r02_epw_direct_fixture_design_contract.json"
PATCH="$ROOT/patches/qe76-epw61-r02-raw-vertex-export.patch"

rm -rf "$WORK" "$EVIDENCE"
mkdir -p "$WORK" "$EVIDENCE"/{build,disabled/commands,enabled/commands,raw,source,validated,runtime}
exec > >(tee -a "$EVIDENCE/runtime/driver.stdout.txt") \
     2> >(tee -a "$EVIDENCE/runtime/driver.stderr.txt" >&2)

status="failed"
stage="initialization"
build_count=0
sequence_count=0
command_count=0
material_calculation_count=0
finish() {
  code=$?
  {
    printf 'status=%s\n' "$status"
    printf 'last_stage=%s\n' "$stage"
    printf 'exit_code=%s\n' "$code"
    printf 'build_count=%s\n' "$build_count"
    printf 'sequence_count=%s\n' "$sequence_count"
    printf 'command_count=%s\n' "$command_count"
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
    Path("first_principles/b0/r02_epw_direct_fixture_execution_contract.json").read_text()
)
design = json.loads(
    Path("first_principles/b0/r02_epw_direct_fixture_design_contract.json").read_text()
)
analysis = json.loads(
    Path("first_principles/b0/r02_epw_raw_vertex_fixture_contract.json").read_text()
)
assert execution["stage"] == "B0_epw_direct_fixture_execution"
assert execution["issue"] == 313
assert execution["phase"] == "one_pinned_execution"
assert execution["design_merge_commit"] == "cd87a414b645a773724ffde9699695954aad36ed"
assert design["issue"] == 309 and design["phase"] == "design_only"
assert analysis["stage"] == "B0_epw_raw_vertex_fixture"
assert analysis["issue"] == 313 and analysis["phase"] == "fixture_execution"
auth = execution["authorization"]
assert auth["source_clone_and_verify"] is True
assert auth["observational_patch_application"] is True
assert auth["exactly_one_pinned_build"] is True
assert auth["exactly_one_disabled_sequence"] is True
assert auth["exactly_one_enabled_sequence"] is True
assert auth["repository_analysis"] is True
assert auth["automatic_retry"] is False
assert auth["testcode_execution"] is False
assert auth["alternate_build"] is False
assert auth["parameter_sweep"] is False
assert auth["soc_fixture"] is False
assert auth["cdte_hgte_or_alloy_calculation"] is False
assert auth["a1_a2_a3"] is False
assert execution["fixture"]["testcode_used"] is False
assert execution["fixture"]["output_discovery_used"] is False
assert execution["fixture"]["outputs_opened_before_process_start"] is True
patch = Path(execution["observational_patch"]["path"])
assert hashlib.sha256(patch.read_bytes()).hexdigest() == execution[
    "observational_patch"
]["sha256"]
PY
cp "$EXECUTION_CONTRACT" "$EVIDENCE/source/execution-contract.json"
cp "$ANALYSIS_CONTRACT" "$EVIDENCE/source/analysis-contract.json"
cp "$DESIGN_CONTRACT" "$EVIDENCE/source/design-contract.json"

stage="focused_tests"
python -m pytest -vv \
  tests/test_r02_epw_direct_fixture_design.py \
  tests/test_r02_epw_raw_vertex_analyzer.py \
  tests/test_r02_epw_direct_fixture_execution.py \
  2>&1 | tee "$EVIDENCE/validated/focused-pytest.txt"

stage="source_clone_and_verify"
SOURCE_COMMIT=$(python - <<'PY'
import json
from pathlib import Path
print(json.loads(Path("first_principles/b0/r02_epw_direct_fixture_execution_contract.json").read_text())["source"]["commit_sha"])
PY
)
SOURCE_URL=$(python - <<'PY'
import json
from pathlib import Path
print(json.loads(Path("first_principles/b0/r02_epw_direct_fixture_execution_contract.json").read_text())["source"]["clone_url"])
PY
)
git init -q "$WORK/qe"
git -C "$WORK/qe" remote add origin "$SOURCE_URL"
git -C "$WORK/qe" fetch --depth 1 origin "$SOURCE_COMMIT"
git -C "$WORK/qe" checkout --detach -q FETCH_HEAD
git -C "$WORK/qe" submodule update --init --recursive --depth 1
test "$(git -C "$WORK/qe" rev-parse HEAD)" = "$SOURCE_COMMIT"

git -C "$WORK/qe" show -s --format=fuller HEAD > "$EVIDENCE/source/commit-metadata.txt"
python - "$WORK/qe" "$EXECUTION_CONTRACT" <<'PY' > r02-epw-direct-fixture-evidence/source/verified-source-manifest.json
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys

repo = Path(sys.argv[1])
contract = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
records = []
for relative, expected_digest in contract["source"]["required_files"].items():
    path = repo / relative
    if not path.is_file():
        raise SystemExit(f"missing pinned source file: {relative}")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != expected_digest:
        raise SystemExit(f"source SHA-256 mismatch for {relative}: {digest}")
    records.append(
        {"path": relative, "sha256": digest, "size_bytes": path.stat().st_size}
    )
print(
    json.dumps(
        {"source_commit": contract["source"]["commit_sha"], "files": records},
        indent=2,
        sort_keys=True,
    )
)
PY
(
  cd "$WORK/qe"
  git archive --format=tar HEAD | sha256sum
) > "$EVIDENCE/source/source-tree-archive-sha256.txt"
test "$(cut -d' ' -f1 "$EVIDENCE/source/source-tree-archive-sha256.txt")" = \
  "$(python - <<'PY'
import json
from pathlib import Path
print(json.loads(Path('first_principles/b0/r02_epw_direct_fixture_execution_contract.json').read_text())['source']['source_tree_archive_sha256'])
PY
)"

test "$(git -C "$WORK/qe" hash-object test-suite/run-epw.sh)" = \
  "$(python - <<'PY'
import json
from pathlib import Path
print(json.loads(Path('first_principles/b0/r02_epw_direct_fixture_execution_contract.json').read_text())['source']['run_epw_git_blob_sha'])
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
for executable in bin/pw.x bin/ph.x bin/epw.x bin/pw2wannier90.x; do
  test -x "$executable"
  sha256sum "$executable" >> "$EVIDENCE/build/executable-sha256.txt"
done
ldd bin/epw.x > "$EVIDENCE/build/epw-ldd.txt" || true

stage="prepare_fixtures_and_manifests"
mkdir -p "$WORK/fixtures"
cp -a "$WORK/qe/test-suite/epw_base" "$WORK/fixtures/disabled"
cp -a "$WORK/qe/test-suite/epw_base" "$WORK/fixtures/enabled"
PW_X="$WORK/qe/bin/pw.x"
PH_X="$WORK/qe/bin/ph.x"
EPW_X="$WORK/qe/bin/epw.x"
EPW_BIN="$WORK/qe/EPW/bin"
PYTHON_X="$(command -v python3)"
export PYTHONPATH="$ROOT"
python - "$DESIGN_CONTRACT" "$WORK/fixtures/disabled" "$EVIDENCE/disabled" \
  "$PW_X" "$PH_X" "$EPW_X" "$PYTHON_X" "$EPW_BIN" <<'PY'
from pathlib import Path
import sys
from tools.design_epw_direct_fixture import build_manifest, load_contract, write_manifest

contract = load_contract(Path(sys.argv[1]))
manifest = build_manifest(
    contract,
    fixture_dir=Path(sys.argv[2]),
    evidence_dir=Path(sys.argv[3]),
    executable_labels={
        "PW_X": sys.argv[4],
        "PH_X": sys.argv[5],
        "EPW_X": sys.argv[6],
        "PYTHON": sys.argv[7],
    },
    epw_bin_dir=Path(sys.argv[8]),
    verify_inputs=True,
)
write_manifest(manifest, Path(sys.argv[3]) / "command-manifest.json")
PY
python - "$DESIGN_CONTRACT" "$WORK/fixtures/enabled" "$EVIDENCE/enabled" \
  "$PW_X" "$PH_X" "$EPW_X" "$PYTHON_X" "$EPW_BIN" <<'PY'
from pathlib import Path
import sys
from tools.design_epw_direct_fixture import build_manifest, load_contract, write_manifest

contract = load_contract(Path(sys.argv[1]))
manifest = build_manifest(
    contract,
    fixture_dir=Path(sys.argv[2]),
    evidence_dir=Path(sys.argv[3]),
    executable_labels={
        "PW_X": sys.argv[4],
        "PH_X": sys.argv[5],
        "EPW_X": sys.argv[6],
        "PYTHON": sys.argv[7],
    },
    epw_bin_dir=Path(sys.argv[8]),
    verify_inputs=True,
)
write_manifest(manifest, Path(sys.argv[3]) / "command-manifest.json")
PY
sha256sum "$EVIDENCE/disabled/command-manifest.json" \
  "$EVIDENCE/enabled/command-manifest.json" \
  > "$EVIDENCE/source/command-manifest-sha256.txt"

run_command() {
  local sequence="$1"
  local fixture="$2"
  local number="$3"
  local identifier="$4"
  local executable="$5"
  local stdin_name="$6"
  shift 6
  local stdout="$EVIDENCE/$sequence/commands/$number-$identifier.stdout.txt"
  local stderr="$EVIDENCE/$sequence/commands/$number-$identifier.stderr.txt"
  printf '# R02 direct fixture command=%s sequence=%s\n' "$identifier" "$sequence" > "$stdout"
  printf '# R02 direct fixture command=%s sequence=%s\n' "$identifier" "$sequence" > "$stderr"
  if [[ "$stdin_name" == "-" ]]; then
    (cd "$fixture" && "$executable" "$@") >> "$stdout" 2>> "$stderr"
  else
    (cd "$fixture" && "$executable" "$@" < "$stdin_name") >> "$stdout" 2>> "$stderr"
  fi
  command_count=$((command_count + 1))
  test -s "$stdout"
  test -s "$stderr"
  printf '%s\n' "$?" > "$EVIDENCE/$sequence/commands/$number-$identifier.exit-code.txt"
}

run_sequence() {
  local sequence="$1"
  local fixture="$WORK/fixtures/$sequence"
  if [[ "$sequence" == "enabled" ]]; then
    export R02_EXPORT_RAW_VERTEX=1
    export R02_EXPORT_IK_GLOBAL=1
    export R02_RAW_VERTEX_PATH="$EVIDENCE/raw/epw-raw-vertex.txt"
  else
    unset R02_EXPORT_RAW_VERTEX R02_EXPORT_IK_GLOBAL R02_RAW_VERTEX_PATH || true
  fi
  run_command "$sequence" "$fixture" 01 pw-scf "$PW_X" - -input scf.in
  run_command "$sequence" "$fixture" 02 ph "$PH_X" - -input ph.in
  run_command "$sequence" "$fixture" 03 pp "$PYTHON_X" pp.in "$EPW_BIN/pp.py"
  run_command "$sequence" "$fixture" 04 pw-scf-epw "$PW_X" - -input scf_epw.in
  run_command "$sequence" "$fixture" 05 pw-nscf-epw "$PW_X" - -input nscf_epw.in
  run_command "$sequence" "$fixture" 06 epw "$EPW_X" - -input epw1.in
  sequence_count=$((sequence_count + 1))
  find "$fixture" -maxdepth 4 -type f -printf '%P %s\n' | sort \
    > "$EVIDENCE/$sequence/generated-files.txt"
}

stage="direct_disabled_sequence"
run_sequence disabled
test "$sequence_count" -eq 1
test "$command_count" -eq 6

stage="direct_enabled_sequence"
rm -f "$EVIDENCE/raw/epw-raw-vertex.txt"
run_sequence enabled
test "$sequence_count" -eq 2
test "$command_count" -eq 12
test -s "$EVIDENCE/raw/epw-raw-vertex.txt"

stage="preservation_gate"
OUTPUT_COUNT=$(find "$EVIDENCE/disabled/commands" "$EVIDENCE/enabled/commands" \
  -type f \( -name '*.stdout.txt' -o -name '*.stderr.txt' \) | wc -l)
test "$OUTPUT_COUNT" -eq 24
printf '%s\n' "$OUTPUT_COUNT" > "$EVIDENCE/runtime/preserved-output-count.txt"
EXIT_COUNT=$(find "$EVIDENCE/disabled/commands" "$EVIDENCE/enabled/commands" \
  -type f -name '*.exit-code.txt' | wc -l)
test "$EXIT_COUNT" -eq 12
printf '%s\n' "$EXIT_COUNT" > "$EVIDENCE/runtime/exit-code-file-count.txt"

stage="analyze"
cd "$ROOT"
python -m tools.analyze_epw_raw_vertex_fixture \
  --raw "$EVIDENCE/raw/epw-raw-vertex.txt" \
  --disabled-stdout "$EVIDENCE/disabled/commands/06-epw.stdout.txt" \
  --enabled-stdout "$EVIDENCE/enabled/commands/06-epw.stdout.txt" \
  --contract "$ANALYSIS_CONTRACT" \
  --output-json "$EVIDENCE/validated/fixture-result.json"

stage="execution_summary"
python - <<'PY' > r02-epw-direct-fixture-evidence/validated/execution-summary.json
import json
from pathlib import Path

result = json.loads(
    Path("r02-epw-direct-fixture-evidence/validated/fixture-result.json").read_text()
)
print(
    json.dumps(
        {
            "schema_version": "1.0",
            "stage": "B0_epw_direct_fixture_execution_summary",
            "issue": 313,
            "status": result["status"],
            "classification": result["decision"]["classification"],
            "build_count": 1,
            "sequence_count": 2,
            "command_count": 12,
            "preserved_stdout_stderr_count": 24,
            "testcode_used": False,
            "output_discovery_used": False,
            "material_calculation_count": 0,
            "analysis_checks": result["checks"],
            "claim_boundary": result["claim_boundary"],
        },
        indent=2,
        sort_keys=True,
    )
)
PY

stage="evidence_volume"
EVIDENCE_BYTES=$(du -sb "$EVIDENCE" | cut -f1)
MAX_BYTES=$(python - <<'PY'
import json
from pathlib import Path
print(json.loads(Path('first_principles/b0/r02_epw_direct_fixture_execution_contract.json').read_text())['thresholds']['maximum_evidence_bytes'])
PY
)
if (( EVIDENCE_BYTES > MAX_BYTES )); then
  echo "evidence exceeds declared ceiling: $EVIDENCE_BYTES > $MAX_BYTES" >&2
  exit 1
fi
printf '%s\n' "$EVIDENCE_BYTES" > "$EVIDENCE/runtime/evidence-size-bytes.txt"

stage="complete"
status="passed"
