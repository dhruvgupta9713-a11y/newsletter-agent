import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_and_status_endpoints():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "system" in data

    res2 = client.get("/api/agent/status")
    assert res2.status_code == 200
    sys_status = res2.json()
    assert "search_provider" in sys_status
    assert "demo_mode" in sys_status

def test_api_run_autonomous_agent():
    payload = {
        "goal": "Build a newsletter highlighting top AI agents and multi-agent coordination.",
        "mode": "autonomous"
    }
    response = client.post("/api/agent/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "run_id" in data
    assert data["status"] == "completed"
    run_id = data["run_id"]

    # Test state retrieval
    state_res = client.get(f"/api/agent/{run_id}")
    assert state_res.status_code == 200
    state = state_res.json()
    assert state["run_id"] == run_id
    assert state["status"] == "completed"
    assert len(state["selected_articles"]) >= 5

    # Test file downloads
    html_res = client.get(f"/api/agent/{run_id}/download/html")
    assert html_res.status_code == 200
    assert "text/html" in html_res.headers.get("content-type", "")

    md_res = client.get(f"/api/agent/{run_id}/download/md")
    assert md_res.status_code == 200
    assert "text/markdown" in md_res.headers.get("content-type", "")

    json_res = client.get(f"/api/agent/{run_id}/download/json")
    assert json_res.status_code == 200
    assert "application/json" in json_res.headers.get("content-type", "")

def test_api_hitl_workflow():
    payload = {
        "goal": "Build an AI agent newsletter with human review.",
        "mode": "hitl"
    }
    response = client.post("/api/agent/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    run_id = data["run_id"]
    assert data["status"] == "waiting_research_approval"

    # Approve research
    approve_res = client.post(
        f"/api/agent/{run_id}/approve-research",
        json={"approved_articles": data["state"]["selected_articles"][:5]}
    )
    assert approve_res.status_code == 200
    approved_data = approve_res.json()
    assert approved_data["status"] == "waiting_newsletter_approval"

    # Approve newsletter
    final_res = client.post(f"/api/agent/{run_id}/approve-newsletter")
    assert final_res.status_code == 200
    assert final_res.json()["status"] == "completed"
