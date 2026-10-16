import pytest
from backend.agent.graph import (
    run_newsletter_agent,
    resume_after_research_approval,
    resume_after_newsletter_approval,
    request_newsletter_revision,
    RUN_STATES
)

def test_autonomous_workflow_complete():
    """Verify that autonomous mode runs to completion without manual input."""
    goal = "Create a newsletter on recent breakthroughs in multi-agent orchestration."
    final_state = run_newsletter_agent(goal=goal, mode="autonomous")
    
    assert final_state["status"] == "completed"
    assert len(final_state["selected_articles"]) >= 5
    assert len(final_state["summaries"]) >= 5
    assert final_state["newsletter_html"] != ""
    assert final_state["newsletter_markdown"] != ""
    assert final_state["critique"] is not None
    assert final_state["critique"]["quality_score"] >= 80
    assert final_state["simulated_delivery"] is not None
    assert final_state["simulated_delivery"]["status"] == "DELIVERED_SIMULATED"
    assert "html_path" in final_state["output_files"]

def test_hitl_mode_research_pause_and_resume():
    """Verify that HITL mode pauses after research, waits for user approval, and resumes."""
    goal = "Create an AI newsletter covering computer use agents."
    initial_state = run_newsletter_agent(goal=goal, mode="hitl")
    run_id = initial_state["run_id"]

    assert initial_state["status"] == "waiting_research_approval"
    assert len(initial_state["selected_articles"]) >= 5
    assert initial_state["research_approved"] is False

    # Simulate user approval with selected articles
    resumed_state = resume_after_research_approval(
        run_id=run_id,
        approved_articles=initial_state["selected_articles"][:5]
    )

    # In HITL, it should now pause at waiting_newsletter_approval
    assert resumed_state["research_approved"] is True
    assert resumed_state["status"] == "waiting_newsletter_approval"
    assert len(resumed_state["summaries"]) == 5
    assert resumed_state["newsletter_html"] != ""

    # Now simulate user approval of newsletter
    final_state = resume_after_newsletter_approval(run_id=run_id)
    assert final_state["status"] == "completed"
    assert final_state["newsletter_approved"] is True
    assert final_state["simulated_delivery"]["status"] == "DELIVERED_SIMULATED"

def test_hitl_revision_request():
    """Verify that user revision feedback is incorporated."""
    goal = "Create an AI newsletter covering coding agents."
    state = run_newsletter_agent(goal=goal, mode="hitl")
    run_id = state["run_id"]
    
    # Approve research
    resumed = resume_after_research_approval(run_id=run_id)
    assert resumed["status"] == "waiting_newsletter_approval"

    # Request revision
    revised = request_newsletter_revision(run_id=run_id, feedback="Emphasize SWE-bench verified benchmark comparisons.")
    assert revised["revision_count"] >= 1
    assert revised["critique"] is not None
