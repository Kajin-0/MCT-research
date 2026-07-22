#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
WORK="${RUNNER_TEMP:-/tmp}/r02-epw-raw-vertex-source-qualification"
EVIDENCE="$ROOT/r02-epw-raw-vertex-source-evidence"
CONTRACT="$ROOT/first_principles/b0/r02_epw_raw_vertex_fixture_contract.json"

rm -rf "$WORK" "$EVIDENCE"
mkdir -p "$WORK" "$EVIDENCE/source" "$EVIDENCE/validated" "$EVIDENCE/runtime"
exec > >(tee -a "$EVIDENCE/runtime/driver.stdout.txt") \
     2> >(tee -a "$EVIDENCE/runtime/driver.stderr.txt" >&2)

status="failed"
stage="initialization"
scientific_execution_count=0
finish() {
  code=$?
  {
    printf 'status=%s\n' "$status"
    printf 'last_stage=%s\n' "$stage"
    printf 'exit_code=%s\n' "$code"
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
  python --version
  sha256sum --version | head -n 1
} > "$EVIDENCE/runtime/system.txt" 2>&1

stage="contract_gate"
python - <<'PY'
import json
from pathlib import Path
contract = json.loads(Path("first_principles/b0/r02_epw_raw_vertex_fixture_contract.json").read_text())
assert contract["stage"] == "B0_epw_raw_vertex_fixture"
assert contract["issue"] == 300
assert contract["phase"] == "source_qualification_only"
auth = contract["authorization"]
assert auth["source_clone_and_hash"] is True
assert auth["qe_epw_build"] is False
assert auth["upstream_fixture_execution"] is False
assert auth["observational_export_patch_application"] is False
assert auth["automatic_phase_transition"] is False
assert all(item["sha256"] is None for item in contract["source"]["required_files"].values())
PY

stage="source_clone"
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
test "$(git -C "$WORK/qe" rev-parse HEAD)" = "$SOURCE_COMMIT"
printf '%s\n' "$SOURCE_COMMIT" > "$EVIDENCE/source/commit.txt"
git -C "$WORK/qe" show -s --format=fuller HEAD > "$EVIDENCE/source/commit-metadata.txt"

stage="verify_blobs_and_hash"
python - "$WORK/qe" "$CONTRACT" "$EVIDENCE/source/source-file-manifest.json" <<'PY'
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1])
contract_path = Path(sys.argv[2])
output = Path(sys.argv[3])
contract = json.loads(contract_path.read_text(encoding="utf-8"))
records = []
for relative, expected in contract["source"]["required_files"].items():
    path = repo / relative
    if not path.is_file():
        raise SystemExit(f"missing required upstream file: {relative}")
    blob = subprocess.check_output(
        ["git", "-C", str(repo), "hash-object", relative], text=True
    ).strip()
    if blob != expected["git_blob_sha"]:
        raise SystemExit(
            f"Git blob mismatch for {relative}: {blob} != {expected['git_blob_sha']}"
        )
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    records.append(
        {
            "path": relative,
            "size_bytes": path.stat().st_size,
            "git_blob_sha": blob,
            "sha256": digest,
        }
    )
manifest = {
    "schema_version": "1.0",
    "stage": "B0_epw_raw_vertex_source_qualification",
    "issue": 300,
    "source_commit": contract["source"]["commit_sha"],
    "scientific_execution_count": 0,
    "qe_epw_build_executed": False,
    "files": records,
}
output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

(
  cd "$WORK/qe"
  git archive --format=tar HEAD | sha256sum
) > "$EVIDENCE/source/source-tree-archive-sha256.txt"

stage="validate_manifest"
python - <<'PY' > r02-epw-raw-vertex-source-evidence/validated/qualification.json
import json
from pathlib import Path
contract = json.loads(Path("first_principles/b0/r02_epw_raw_vertex_fixture_contract.json").read_text())
manifest = json.loads(Path("r02-epw-raw-vertex-source-evidence/source/source-file-manifest.json").read_text())
assert manifest["source_commit"] == contract["source"]["commit_sha"]
assert manifest["scientific_execution_count"] == 0
assert manifest["qe_epw_build_executed"] is False
expected = contract["source"]["required_files"]
observed = {item["path"]: item for item in manifest["files"]}
assert set(observed) == set(expected)
for path, specification in expected.items():
    assert observed[path]["git_blob_sha"] == specification["git_blob_sha"]
    assert len(observed[path]["sha256"]) == 64
    assert observed[path]["size_bytes"] > 0
print(json.dumps({
    "passed": True,
    "phase": contract["phase"],
    "file_count": len(observed),
    "scientific_execution_count": 0,
    "phase_2_automatically_authorized": False,
}, indent=2, sort_keys=True))
PY

stage="complete"
status="passed"
