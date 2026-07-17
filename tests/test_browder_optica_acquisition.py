from __future__ import annotations

import json
from pathlib import Path

from acquire_browder_optica_table import (
    TableParser,
    canonical_rows_digest,
    find_cdte_rows,
    load_committed_rows,
    normalize_text,
)


def test_table_parser_recovers_numeric_rows() -> None:
    parser = TableParser()
    parser.feed(
        """
        <table>
          <tr><th>T(K)</th><th>CdTe (Irtran 6)</th></tr>
          <tr><td>10</td><td>−0.47</td></tr>
          <tr><td>15</td><td>−1.15</td></tr>
        </table>
        """
    )
    assert parser.tables[0][1:] == [["10", "−0.47"], ["15", "−1.15"]]


def test_find_cdte_rows_selects_long_numeric_table() -> None:
    table = [["T", "CdTe"]] + [[str(index), str(index / 10)] for index in range(25)]
    rows = find_cdte_rows([[["x"]], table])
    assert len(rows) == 25
    assert rows[0] == (0.0, 0.0)
    assert rows[-1] == (24.0, 2.4)


def test_committed_browder_table_identity() -> None:
    rows = load_committed_rows(
        Path("data/experimental/browder1972_cdte_irtran6_alpha.csv")
    )
    assert len(rows) == 25
    assert rows[0] == (10.0, -0.47)
    assert rows[-1] == (300.0, 5.3)
    assert len(canonical_rows_digest(rows)) == 64


def test_acquisition_contract_is_digest_only() -> None:
    contract = json.loads(
        Path("literature/browder1972_optica_table_acquisition_contract.json").read_text(
            encoding="utf-8"
        )
    )
    assert contract["citation"]["doi"] == "10.1364/AO.11.000841"
    assert contract["table_validation"]["expected_row_count"] == 25
    assert contract["rights_and_storage"] == {
        "commit_publisher_html": False,
        "upload_publisher_html_as_artifact": False,
        "preserve_only_digest_metadata_and_table_validation": True,
    }
    assert normalize_text("CdTe (Irtran 6)") == "cdte (irtran 6)"
