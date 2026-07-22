from __future__ import annotations

import subprocess
from pathlib import Path


STATE_PATH = Path("research/programs/empirical_bandgap/state.md")
EXPECTED_BLOB = "4a87eaccbbd1acbca8d39c14a00199514c4ba83c"


def _blob_sha(path: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(path)], text=True
    ).strip()


def _replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected one replacement target, found {count}: {old!r}")
    return text.replace(old, new, 1)


def main() -> None:
    actual_blob = _blob_sha(STATE_PATH)
    if actual_blob != EXPECTED_BLOB:
        raise RuntimeError(
            f"refusing state synchronization: expected blob {EXPECTED_BLOB}, "
            f"found {actual_blob}"
        )

    text = STATE_PATH.read_text(encoding="utf-8")

    replacements = [
        (
            "- #283 — Finkman and Nemirovsky 1979 optical-absorption source audit.\n",
            "- #283 — Finkman and Nemirovsky 1979 optical-absorption source audit;\n"
            "- #293 — Weiler 1981 HSC_R04 source-lineage reconciliation.\n",
        ),
        (
            "- provenance-controlled Finkman and Nemirovsky 1979 optical-absorption source audit.\n",
            "- provenance-controlled Finkman and Nemirovsky 1979 optical-absorption source audit;\n"
            "- fail-closed Weiler 1981 HSC_R04 chapter-lineage and private-composition provenance reconciliation.\n",
        ),
        (
            "- what datum-level evidence and edge definitions Hansen actually fitted across the remaining source graph;\n",
            "- what datum-level evidence and edge definitions Hansen actually fitted across the remaining source graph;\n"
            "- whether an authorized Weiler 1981 chapter copy can establish the chapter-to-1977 specimen and temperature-series mapping;\n"
            "- whether the Micklethwaite private compositions adopted by Hansen or the Reine density alternatives can be recovered from a traceable specimen-level source;\n",
        ),
        (
            "The Seiler, Camassel, Scott, Blue, Groves, and Schmit source results do not authorize manuscript writing by themselves.\n",
            "The Seiler, Camassel, Scott, Blue, Groves, Schmit, Finkman, and Weiler source results do not authorize manuscript writing by themselves.\n",
        ),
        (
            "- continue the Hansen source-by-source specimen reconstruction;\n",
            "- continue the Hansen source-by-source specimen reconstruction;\n"
            "- obtain an authorized full-text copy of Weiler 1981 before any HSC_R04 numerical reconstruction;\n"
            "- preserve published Weiler, Micklethwaite private, and Reine private composition layers separately;\n",
        ),
        (
            "- digitizing Finkman Figures 3–6 as a model-independent logarithmic-curvature validation dataset;\n",
            "- digitizing Finkman Figures 3–6 as a model-independent logarithmic-curvature validation dataset;\n"
            "- treating the published Weiler 1977 compositions as the per-specimen values actually ingested by Hansen under HSC_R04;\n"
            "- reconstructing Micklethwaite private compositions by applying the Reine `+0.01` to `+0.035` range to published specimens;\n"
            "- treating the Reine range as a universal composition correction;\n"
            "- claiming one-to-one specimen identity or numerical chapter reconstruction for Weiler 1981 without the chapter full text;\n",
        ),
    ]

    for old, new in replacements:
        text = _replace_once(text, old, new)

    marker = "## Unresolved scientific questions\n"
    if text.count(marker) != 1:
        raise RuntimeError("unresolved-science marker is not unique")

    section = """## Weiler 1981 HSC_R04 source-lineage reconciliation

Issue #293 and draft PR #295 establish a fail-closed source contract for Hansen fitted source `HSC_R04`.

Canonical files are:

```text
data/hansen/weiler1981_hsc_r04_source_metadata.csv
data/hansen/weiler1981_hsc_r04_composition_provenance.csv
data/hansen/weiler1981_hsc_r04_README.md
```

### Exact source and access state

Hansen cites

```text
M. H. Weiler
Magnetooptical Properties of Hg1-xCdxTe Alloys
Semiconductors and Semimetals 16, 119-191 (1981)
DOI 10.1016/S0080-8784(08)60130-1
```

Publisher metadata and summary are available, but the chapter full text is not present in the user File Library or repository runtime. No chapter hash, table, figure, specimen registry, or numerical series is fabricated.

### Existing 1977 evidence lineage

PR #158 already audits the primary Weiler, Aggarwal, and Lax 1977 magnetoreflectance paper in

```text
data/evidence/guldner_weiler_1977_magneto_core.json
```

The 1981 chapter is likely part of that scientific lineage, but the available evidence does not prove one-to-one identity between every chapter datum and the ten 1977 specimens. The existing evidence record is linked and remains unchanged.

### Three composition-provenance layers

The repository retains separately:

```text
Weiler 1977 published compositions
Micklethwaite private transmission-cutoff compositions adopted by Hansen
Reine private density alternatives reported as +0.01 to +0.035 higher
```

The private per-specimen values are unavailable. The Reine range is provenance context, not a transformation rule. No shifted or reconstructed private composition table is authorized.

### Numerical and claim boundary

```text
HSC_R04 numerical reconstruction = blocked
chapter-to-1977 specimen mapping = unresolved
temperature-series mapping = unresolved
private composition reconstruction = prohibited
chapter figure digitization = prohibited in this tranche
```

The focused lineage workflow and both complete Python suites passed before this ledger synchronization. This result establishes source identity and a provenance boundary; it does not supply new gap observations, fit coefficients, composition corrections, or model ranking.

"""
    text = text.replace(marker, section + marker, 1)

    required = [
        "#293 — Weiler 1981 HSC_R04 source-lineage reconciliation",
        "## Weiler 1981 HSC_R04 source-lineage reconciliation",
        "HSC_R04 numerical reconstruction = blocked",
        "private composition reconstruction = prohibited",
        "The Reine range is provenance context, not a transformation rule",
    ]
    for phrase in required:
        if phrase not in text:
            raise RuntimeError(f"missing synchronized phrase: {phrase}")

    if text.strip() == "hello" or len(text.splitlines()) < 900:
        raise RuntimeError("canonical R01 ledger is truncated")

    STATE_PATH.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
