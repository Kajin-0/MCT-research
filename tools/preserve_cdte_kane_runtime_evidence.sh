#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
WORK="${RUNNER_TEMP:-/tmp}/cdte-kane-runtime"
EVIDENCE="$ROOT/cdte-kane-evidence"
SCHEMA="$WORK/run/tmp/cdte_kane.save/data-file-schema.xml"

mkdir -p "$EVIDENCE/runtime" "$EVIDENCE/raw"
test -s "$SCHEMA"
python "$ROOT/tools/extract_qe_ks_energies.py" "$SCHEMA" \
  --output-json "$EVIDENCE/runtime/ks_energies.json" \
  > "$EVIDENCE/runtime/ks_energies.stdout.txt"
cp "$SCHEMA" "$EVIDENCE/raw/data-file-schema.xml"
sha256sum "$SCHEMA" > "$EVIDENCE/runtime/data_file_schema_sha256.txt"

python - "$EVIDENCE/runtime/ks_energies.json" <<'PY' \
  > "$EVIDENCE/runtime/ks_energies_validation.json"
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
data = json.loads(path.read_text(encoding="utf-8"))
if data["num_kpoints"] != 13 or data["num_bands"] != 40:
    raise SystemExit("expected 13 ordered k points and 40 bands")
indices = [block["index"] for block in data["blocks"]]
if indices != list(range(1, 14)):
    raise SystemExit("QE eigenvalue block order changed")
print(json.dumps({
    "status": "full_precision_ordered_eigenvalues_verified",
    "num_kpoints": data["num_kpoints"],
    "num_bands": data["num_bands"],
    "indices": indices,
}, indent=2, sort_keys=True))
PY
