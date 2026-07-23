#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
WORK="${RUNNER_TEMP:-/tmp}/r02-epw-raw-vertex-fixture"
EVIDENCE="$ROOT/r02-epw-raw-vertex-fixture-evidence"
CONTRACT="$ROOT/first_principles/b0/r02_epw_raw_vertex_fixture_contract.json"
PATCH="$ROOT/patches/qe76-epw61-r02-raw-vertex-export.patch"
CAPTURE_HELPER="$WORK/capture_epw_test_output.py"

rm -rf "$WORK" "$EVIDENCE"
mkdir -p "$WORK" "$EVIDENCE"/{build,disabled,enabled,raw,validated,runtime,source}
exec > >(tee -a "$EVIDENCE/runtime/driver.stdout.txt") \
     2> >(tee -a "$EVIDENCE/runtime/driver.stderr.txt" >&2)

status="failed"
stage="initialization"
scientific_execution_count=0
build_count=0
finish() {
  code=$?
  {
    printf 'status=%s\n' "$status"
    printf 'last_stage=%s\n' "$stage"
    printf 'exit_code=%s\n' "$code"
    printf 'build_count=%s\n' "$build_count"
    printf 'scientific_execution_count=%s\n' "$scientific_execution_count"
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
contract = json.loads(Path("first_principles/b0/r02_epw_raw_vertex_fixture_contract.json").read_text())
assert contract["stage"] == "B0_epw_raw_vertex_fixture"
assert contract["issue"] == 300
assert contract["phase"] == "fixture_execution"
auth = contract["authorization"]
assert auth["qe_epw_build"] is True
assert auth["upstream_fixture_execution"] is True
assert auth["observational_export_patch_application"] is True
assert auth["exactly_one_pinned_build"] is True
assert auth["exactly_two_fixture_runs_same_state"] is True
assert auth["automatic_retry"] is False
assert auth["cdte_hgte_or_alloy_calculation"] is False
assert auth["a1_a2_a3"] is False
assert all(len(item["sha256"]) == 64 for item in contract["source"]["required_files"].values())
patch = Path(contract["observational_patch"]["path"])
assert hashlib.sha256(patch.read_bytes()).hexdigest() == contract["observational_patch"]["sha256"]
assert contract["fixture"]["material"] == "diamond"
assert contract["fixture"]["long_range_included"] is False
assert contract["fixture"]["epsilon_response_enabled"] is False
PY

stage="capture_locator_definition"
cat > "$CAPTURE_HELPER" <<'PY'
from __future__ import annotations

import argparse
import shutil
import tempfile
from pathlib import Path

STDOUT_GLOB = "test.out.*.inp=epw1.in.args=3"
STDERR_PREFIX_FROM = "test.out."
STDERR_PREFIX_TO = "test.err."


class CaptureError(RuntimeError):
    pass


def locate_unique_pair(root: Path) -> tuple[Path, Path]:
    candidates = sorted(path for path in root.glob(STDOUT_GLOB) if path.is_file())
    if len(candidates) != 1:
        rendered = ", ".join(path.name for path in candidates) or "none"
        raise CaptureError(
            f"expected exactly one {STDOUT_GLOB!r} in {root}, "
            f"found {len(candidates)}: {rendered}"
        )
    stdout = candidates[0]
    stderr = root / stdout.name.replace(STDERR_PREFIX_FROM, STDERR_PREFIX_TO, 1)
    if not stderr.is_file():
        raise CaptureError(f"missing matching EPW stderr file: {stderr}")
    if stdout.stat().st_size == 0:
        raise CaptureError(f"EPW stdout is empty: {stdout}")
    return stdout, stderr


def capture_pair(
    root: Path,
    stdout_destination: Path,
    stderr_destination: Path,
) -> tuple[Path, Path]:
    stdout, stderr = locate_unique_pair(root)
    stdout_destination.parent.mkdir(parents=True, exist_ok=True)
    stderr_destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(stdout, stdout_destination)
    shutil.copy2(stderr, stderr_destination)
    stdout_destination.with_suffix(stdout_destination.suffix + ".source-path.txt").write_text(
        str(stdout) + "\n",
        encoding="utf-8",
    )
    stderr_destination.with_suffix(stderr_destination.suffix + ".source-path.txt").write_text(
        str(stderr) + "\n",
        encoding="utf-8",
    )
    return stdout, stderr


def self_test() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        try:
            locate_unique_pair(root)
        except CaptureError as error:
            assert "found 0" in str(error)
        else:
            raise AssertionError("zero-match case did not fail closed")

        stdout = root / "test.out.220726.inp=epw1.in.args=3"
        stderr = root / "test.err.220726.inp=epw1.in.args=3"
        stdout.write_text("EPW stdout\n", encoding="utf-8")
        stderr.write_text("EPW stderr\n", encoding="utf-8")
        out_copy = root / "captured" / "epw1.stdout.txt"
        err_copy = root / "captured" / "epw1.stderr.txt"
        capture_pair(root, out_copy, err_copy)
        assert out_copy.read_text(encoding="utf-8") == "EPW stdout\n"
        assert err_copy.read_text(encoding="utf-8") == "EPW stderr\n"

        second_stdout = root / "test.out.220727.inp=epw1.in.args=3"
        second_stderr = root / "test.err.220727.inp=epw1.in.args=3"
        second_stdout.write_text("second\n", encoding="utf-8")
        second_stderr.write_text("second err\n", encoding="utf-8")
        try:
            locate_unique_pair(root)
        except CaptureError as error:
            assert "found 2" in str(error)
        else:
            raise AssertionError("multiple-match case did not fail closed")

        second_stdout.unlink()
        second_stderr.unlink()
        stderr.unlink()
        try:
            locate_unique_pair(root)
        except CaptureError as error:
            assert "missing matching EPW stderr" in str(error)
        else:
            raise AssertionError("missing-stderr case did not fail closed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path)
    parser.add_argument("--stdout-destination", type=Path)
    parser.add_argument("--stderr-destination", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.root is None or args.stdout_destination is None or args.stderr_destination is None:
        parser.error("--root, --stdout-destination, and --stderr-destination are required")
    capture_pair(args.root, args.stdout_destination, args.stderr_destination)


if __name__ == "__main__":
    main()
PY

stage="focused_tests"
python "$CAPTURE_HELPER" --self-test \
  2>&1 | tee "$EVIDENCE/validated/capture-locator-self-test.txt"
python -m pytest -vv \
  tests/test_r02_epw_raw_vertex_source_gate.py \
  tests/test_r02_epw_raw_vertex_analyzer.py \
  2>&1 | tee "$EVIDENCE/validated/focused-pytest.txt"

stage="source_clone_and_verify"
SOURCE_COMMIT=$(python - <<'PY'
import json
from pathlib import Path
print(json.loads(Path("first_principles/b0/r02_epw_raw_vertex_fixture_contract.json").read_text())["source"]["commit_sha"])
PY
)
SOURCE_URL=$(python - <<'PY'
import json
from pathlib import Path
print(json.loads(Path("first_principles/b0/r02_epw_raw_vertex_fixture_contract.json").read_text())["source"]["clone_url"])
PY
)
git init -q "$WORK/qe"
git -C "$WORK/qe" remote add origin "$SOURCE_URL"
git -C "$WORK/qe" fetch --depth 1 origin "$SOURCE_COMMIT"
git -C "$WORK/qe" checkout --detach -q FETCH_HEAD
git -C "$WORK/qe" submodule update --init --recursive --depth 1
test "$(git -C "$WORK/qe" rev-parse HEAD)" = "$SOURCE_COMMIT"

python - "$WORK/qe" "$CONTRACT" <<'PY' > r02-epw-raw-vertex-fixture-evidence/source/verified-source-manifest.json
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys
repo = Path(sys.argv[1])
contract = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
records = []
for relative, expected in contract["source"]["required_files"].items():
    path = repo / relative
    blob = subprocess.check_output(["git", "-C", str(repo), "hash-object", relative], text=True).strip()
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if blob != expected["git_blob_sha"] or digest != expected["sha256"]:
        raise SystemExit(f"pinned source mismatch: {relative}")
    records.append({"path": relative, "git_blob_sha": blob, "sha256": digest, "size_bytes": path.stat().st_size})
print(json.dumps({"source_commit": contract["source"]["commit_sha"], "files": records}, indent=2, sort_keys=True))
PY
(
  cd "$WORK/qe"
  git archive --format=tar HEAD | sha256sum
) > "$EVIDENCE/source/source-tree-archive-sha256.txt"
test "$(cut -d' ' -f1 "$EVIDENCE/source/source-tree-archive-sha256.txt")" = \
  "$(python - <<'PY'
import json
from pathlib import Path
print(json.loads(Path('first_principles/b0/r02_epw_raw_vertex_fixture_contract.json').read_text())['source']['source_tree_archive_sha256'])
PY
)"

stage="apply_observational_patch"
git -C "$WORK/qe" apply --check "$PATCH"
git -C "$WORK/qe" apply "$PATCH"
git -C "$WORK/qe" diff --check
git -C "$WORK/qe" diff -- EPW/src/selfen.f90 > "$EVIDENCE/source/applied-observational.patch"
sha256sum "$PATCH" "$EVIDENCE/source/applied-observational.patch" \
  > "$EVIDENCE/source/patch-sha256.txt"

stage="prepare_custom_fixture"
FIXTURE="$WORK/qe/test-suite/r02_epw_raw_vertex"
cp -a "$WORK/qe/test-suite/epw_base" "$FIXTURE"
cat >> "$WORK/qe/test-suite/jobconfig" <<'EOF'

[r02_epw_raw_vertex/]
program = EPW
inputs_args = ('scf.in', '1'), ('ph.in', '2'), ('scf_epw.in', '1'), ('nscf_epw.in', '1'), ('epw1.in', '3')
EOF

stage="configure_and_build"
build_count=1
cd "$WORK/qe"
./configure --disable-parallel --enable-openmp \
  2>&1 | tee "$EVIDENCE/build/configure.txt"
make -j2 pw ph epw \
  2>&1 | tee "$EVIDENCE/build/make.txt"
for executable in bin/pw.x bin/ph.x bin/epw.x bin/pw2wannier90.x; do
  test -x "$executable"
  sha256sum "$executable" >> "$EVIDENCE/build/executable-sha256.txt"
done
ldd bin/epw.x > "$EVIDENCE/build/epw-ldd.txt" || true

capture_epw_output() {
  local destination="$1"
  python "$CAPTURE_HELPER" \
    --root "$WORK/qe/test-suite" \
    --stdout-destination "$destination/epw1.stdout.txt" \
    --stderr-destination "$destination/epw1.stderr.txt"
}

run_fixture() {
  local mode="$1"
  local destination="$2"
  make -C "$WORK/qe/test-suite" clean >/dev/null 2>&1 || true
  rm -f "$EVIDENCE/raw/epw-raw-vertex.txt"
  export OMP_NUM_THREADS=1
  export OPENBLAS_NUM_THREADS=1
  export MKL_NUM_THREADS=1
  if [[ "$mode" == "enabled" ]]; then
    export R02_EXPORT_RAW_VERTEX=1
    export R02_RAW_VERTEX_PATH="$EVIDENCE/raw/epw-raw-vertex.txt"
    export R02_EXPORT_IK_GLOBAL=1
  else
    unset R02_EXPORT_RAW_VERTEX R02_RAW_VERTEX_PATH R02_EXPORT_IK_GLOBAL || true
  fi
  scientific_execution_count=$((scientific_execution_count + 1))
  make -C "$WORK/qe/test-suite" run-custom-test testdir=r02_epw_raw_vertex \
    2>&1 | tee "$destination/test-suite-driver.txt"
  capture_epw_output "$destination"
  find "$FIXTURE" -maxdepth 3 -type f -printf '%P %s\n' | sort \
    > "$destination/generated-files.txt"
  find "$WORK/qe/test-suite" -maxdepth 1 -type f \
    \( -name 'test.out.*.inp=epw1.in.args=3' -o -name 'test.err.*.inp=epw1.in.args=3' \) \
    -printf '%f %s\n' | sort > "$destination/epw-generated-files.txt"
}

stage="fixture_disabled"
run_fixture disabled "$EVIDENCE/disabled"
test "$scientific_execution_count" -eq 1

stage="fixture_enabled"
run_fixture enabled "$EVIDENCE/enabled"
test "$scientific_execution_count" -eq 2
test -s "$EVIDENCE/raw/epw-raw-vertex.txt"

stage="analyze"
cd "$ROOT"
python -m tools.analyze_epw_raw_vertex_fixture \
  --raw "$EVIDENCE/raw/epw-raw-vertex.txt" \
  --disabled-stdout "$EVIDENCE/disabled/epw1.stdout.txt" \
  --enabled-stdout "$EVIDENCE/enabled/epw1.stdout.txt" \
  --contract "$CONTRACT" \
  --output-json "$EVIDENCE/validated/fixture-result.json"

stage="evidence_volume"
EVIDENCE_BYTES=$(du -sb "$EVIDENCE" | cut -f1)
MAX_BYTES=$(python - <<'PY'
import json
from pathlib import Path
print(json.loads(Path('first_principles/b0/r02_epw_raw_vertex_fixture_contract.json').read_text())['thresholds']['maximum_evidence_bytes'])
PY
)
if (( EVIDENCE_BYTES > MAX_BYTES )); then
  echo "evidence exceeds declared ceiling: $EVIDENCE_BYTES > $MAX_BYTES" >&2
  exit 1
fi
printf '%s\n' "$EVIDENCE_BYTES" > "$EVIDENCE/runtime/evidence-size-bytes.txt"

stage="complete"
status="passed"
