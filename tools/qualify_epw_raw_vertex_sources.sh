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
assert contract["phase"] in {"source_qualification_only", "fixture_execution"}
auth = contract["authorization"]
assert auth["source_clone_and_hash"] is True
assert auth["automatic_phase_transition"] is False
if contract["phase"] == "source_qualification_only":
    assert auth["qe_epw_build"] is False
    assert auth["upstream_fixture_execution"] is False
    assert auth["observational_export_patch_application"] is False
    assert all(item["sha256"] is None for item in contract["source"]["required_files"].values())
    assert contract["observational_patch"]["sha256"] is None
else:
    assert auth["qe_epw_build"] is True
    assert auth["upstream_fixture_execution"] is True
    assert auth["observational_export_patch_application"] is True
    assert all(len(item["sha256"]) == 64 for item in contract["source"]["required_files"].values())
    assert len(contract["observational_patch"]["sha256"]) == 64
assert contract["observational_patch"]["disabled_by_default"] is True
assert contract["observational_patch"]["scientific_contraction_added"] is False
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
python - "$WORK/qe" "$CONTRACT" "$ROOT" \
  "$EVIDENCE/source/source-file-manifest.json" <<'PY'
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1])
contract_path = Path(sys.argv[2])
root = Path(sys.argv[3])
output = Path(sys.argv[4])
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
    if expected["sha256"] is not None and digest != expected["sha256"]:
        raise SystemExit(
            f"SHA-256 mismatch for {relative}: {digest} != {expected['sha256']}"
        )
    records.append(
        {
            "path": relative,
            "size_bytes": path.stat().st_size,
            "git_blob_sha": blob,
            "sha256": digest,
        }
    )
patch_path = root / contract["observational_patch"]["path"]
if not patch_path.is_file():
    raise SystemExit(f"missing observational patch: {patch_path}")
patch_digest = hashlib.sha256(patch_path.read_bytes()).hexdigest()
expected_patch_digest = contract["observational_patch"]["sha256"]
if expected_patch_digest is not None and patch_digest != expected_patch_digest:
    raise SystemExit(
        f"patch SHA-256 mismatch: {patch_digest} != {expected_patch_digest}"
    )
patch_record = {
    "path": contract["observational_patch"]["path"],
    "size_bytes": patch_path.stat().st_size,
    "sha256": patch_digest,
}
manifest = {
    "schema_version": "1.0",
    "stage": "B0_epw_raw_vertex_source_qualification",
    "issue": 300,
    "contract_phase": contract["phase"],
    "source_commit": contract["source"]["commit_sha"],
    "scientific_execution_count": 0,
    "qe_epw_build_executed": False,
    "files": records,
    "observational_patch": patch_record,
}
output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

(
  cd "$WORK/qe"
  git archive --format=tar HEAD | sha256sum
) > "$EVIDENCE/source/source-tree-archive-sha256.txt"
TREE_DIGEST=$(cut -d' ' -f1 "$EVIDENCE/source/source-tree-archive-sha256.txt")
EXPECTED_TREE_DIGEST=$(python - <<'PY'
import json
from pathlib import Path
value = json.loads(Path("first_principles/b0/r02_epw_raw_vertex_fixture_contract.json").read_text())["source"].get("source_tree_archive_sha256")
print(value or "")
PY
)
if [[ -n "$EXPECTED_TREE_DIGEST" && "$TREE_DIGEST" != "$EXPECTED_TREE_DIGEST" ]]; then
  echo "source tree archive SHA-256 mismatch" >&2
  exit 1
fi

stage="validate_manifest"
python - <<'PY' > r02-epw-raw-vertex-source-evidence/validated/qualification.json
import json
from pathlib import Path
contract = json.loads(Path("first_principles/b0/r02_epw_raw_vertex_fixture_contract.json").read_text())
manifest = json.loads(Path("r02-epw-raw-vertex-source-evidence/source/source-file-manifest.json").read_text())
assert manifest["source_commit"] == contract["source"]["commit_sha"]
assert manifest["contract_phase"] == contract["phase"]
assert manifest["scientific_execution_count"] == 0
assert manifest["qe_epw_build_executed"] is False
expected = contract["source"]["required_files"]
observed = {item["path"]: item for item in manifest["files"]}
assert set(observed) == set(expected)
for path, specification in expected.items():
    assert observed[path]["git_blob_sha"] == specification["git_blob_sha"]
    assert len(observed[path]["sha256"]) == 64
    if specification["sha256"] is not None:
        assert observed[path]["sha256"] == specification["sha256"]
    assert observed[path]["size_bytes"] > 0
patch = manifest["observational_patch"]
assert patch["path"] == contract["observational_patch"]["path"]
assert len(patch["sha256"]) == 64
if contract["observational_patch"]["sha256"] is not None:
    assert patch["sha256"] == contract["observational_patch"]["sha256"]
assert patch["size_bytes"] > 0
print(json.dumps({
    "passed": True,
    "phase": contract["phase"],
    "file_count": len(observed),
    "observational_patch_hashed": True,
    "scientific_execution_count": 0,
    "phase_2_automatically_authorized": False,
}, indent=2, sort_keys=True))
PY

stage="complete"
status="passed"
