"""Tests for medication interaction checker."""

from patient_advocacy.services.interactions import check_interactions, check_pair, _normalize


def test_normalize():
    assert _normalize("Metformin") == "metformin"
    assert _normalize("  Lisinopril ") == "lisinopril"


def test_check_pair_known():
    result = check_pair("warfarin", "aspirin")
    assert result.found is True
    assert result.severity == "severe"


def test_check_pair_unknown():
    result = check_pair("vitamin_c", "zinc")
    assert result.found is False
    assert result.severity == "unknown"


def test_check_interactions_multiple():
    results = check_interactions(["warfarin", "aspirin", "ibuprofen"])
    assert len(results) >= 2  # warfarin+aspirin and warfarin+ibuprofen
    severities = {r.severity for r in results}
    assert "severe" in severities


def test_check_interactions_no_matches():
    results = check_interactions(["vitamin_d", "calcium"])
    assert len(results) == 0


def test_check_interactions_single_drug():
    results = check_interactions(["metformin"])
    assert len(results) == 0
