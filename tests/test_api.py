"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from patient_advocacy.api import app


client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
    assert resp.json()["privacy"] == "all-local"


def test_list_states():
    resp = client.get("/rights")
    assert resp.status_code == 200
    assert "CA" in resp.json()["available_states"]


def test_get_rights_api():
    resp = client.get("/rights/CA")
    assert resp.status_code == 200
    assert resp.json()["state"] == "CA"
    assert len(resp.json()["rights"]) > 0


def test_check_interactions_api():
    resp = client.post("/interactions", json={"drugs": ["warfarin", "aspirin"]})
    assert resp.status_code == 200
    assert len(resp.json()["interactions"]) > 0
    assert resp.json()["interactions"][0]["severity"] == "severe"
