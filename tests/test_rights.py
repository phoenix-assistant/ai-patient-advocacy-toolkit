"""Tests for rights navigator."""

from patient_advocacy.services.rights import get_rights, get_available_states


def test_get_rights_ca():
    rights = get_rights("CA")
    assert len(rights) > 0
    categories = {r["category"] for r in rights}
    assert "HIPAA" in categories


def test_get_rights_ny():
    rights = get_rights("NY")
    assert len(rights) > 0
    titles = {r["title"] for r in rights}
    assert "NY Patient Bill of Rights" in titles


def test_get_rights_includes_federal():
    rights = get_rights("CA")
    # Federal rights should be included
    sources = {r["title"] for r in rights}
    assert "EMTALA" in sources


def test_get_rights_unknown_state():
    rights = get_rights("ZZ")
    assert len(rights) > 0
    # Should still include federal rights
    assert any("Federal" in r.get("title", "") or r["category"] == "Info" for r in rights)


def test_get_rights_case_insensitive():
    rights_upper = get_rights("CA")
    rights_lower = get_rights("ca")
    assert len(rights_upper) == len(rights_lower)


def test_available_states():
    states = get_available_states()
    assert "CA" in states
    assert "NY" in states
    assert "_FEDERAL" not in states
