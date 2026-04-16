"""Smoke tests: app factory, health, blueprint wiring (no external APIs)."""

from __future__ import annotations


def test_health_ok(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data is not None
    assert data.get("status") == "ok"
    assert "StrangeVerse" in (data.get("service") or "")


def test_api_graph_project_list_route_registered(client):
    """Blueprint mounted; may 401/500 without Zep but must not 404 on route."""
    res = client.get("/api/graph/project/list")
    assert res.status_code != 404


def test_api_simulation_list_route_registered(client):
    res = client.get("/api/simulation/list")
    assert res.status_code != 404


def test_optimize_interview_prompt_prefix():
    from app.api.simulation import INTERVIEW_PROMPT_PREFIX, optimize_interview_prompt

    raw = "What do you think?"
    out = optimize_interview_prompt(raw)
    assert out.startswith(INTERVIEW_PROMPT_PREFIX)
    assert raw in out
    # Idempotent
    assert optimize_interview_prompt(out) == out
