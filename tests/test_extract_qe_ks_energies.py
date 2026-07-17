from pathlib import Path
from tools.extract_qe_ks_energies import extract


def test_extract_qe_ks_energies(tmp_path: Path):
    xml = tmp_path / "schema.xml"
    xml.write_text("""<q:root xmlns:q='urn:q'><q:ks_energies><q:k_point weight='1'>0 0 0</q:k_point><q:eigenvalues>-0.5 0.25</q:eigenvalues><q:occupations>1 0</q:occupations></q:ks_energies></q:root>""")
    result = extract(xml)
    assert (result["num_kpoints"], result["num_bands"]) == (1, 2)
    assert result["blocks"][0]["k_point_crystal"] == [0.0, 0.0, 0.0]
