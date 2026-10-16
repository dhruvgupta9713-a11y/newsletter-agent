import uuid
import time
from typing import Dict, Any, Optional
from langgraph.graph import StateGraph, END
from backend.agent.state import AgentState
from backend.agent.nodes import (
    plan_node,
    research_node,
    summarize_node,
    write_node,
    critique_node,
    revise_node,
    send_simulation_node
)

def create_initial_state(goal: str, mode: str = "autonomous", run_id: Optional[str] = None) -> AgentState:
    """Instantiate a pristine agent workflow state."""
    return {
        "run_id": run_id or f"run_{uuid.uuid4().hex[:8]}",
        "goal": goal,
        "mode": mode.lower(),
        "plan": None,
        "search_queries": [],
        "raw_articles": [],
        "selected_articles": [],
        "research_approved": False,
        "summaries": [],
        "newsletter_title": "",
        "subject_line": "",
        "newsletter_html": "",
        "newsletter_markdown": "",
        "newsletter_approved": False,
        "critique": None,
        "revision_count": 0,
        "revision_feedback": None,
        "simulated_delivery": None,
        "output_files": {},
        "logs": [],
        "current_step": "initialized",
        "status": "planning",
        "error": None,
        "start_time": time.time(),
        "duration_seconds": 0.0
    }

def route_after_research(state: AgentState) -> str:
    """Conditional router following the research phase."""
    if state.get("status") == "waiting_research_approval":
        return END
    return "summarize"

def route_after_critique(state: AgentState) -> str:
    """Conditional router following self-critique."""
    status = state.get("status")
    if status == "revising":
        return "revise"
    elif status == "waiting_newsletter_approval":
        return END
    return "send_simulation"

def build_newsletter_graph() -> StateGraph:
    """Constructs the executable LangGraph workflow."""
    workflow = StateGraph(AgentState)

    # Add workflow nodes
    workflow.add_node("plan", plan_node)
    workflow.add_node("research", research_node)
    workflow.add_node("summarize", summarize_node)
    workflow.add_node("write", write_node)
    workflow.add_node("critique", critique_node)
    workflow.add_node("revise", revise_node)
    workflow.add_node("send_simulation", send_simulation_node)

    # Define edges and conditional transitions
    workflow.set_entry_point("plan")
    workflow.add_edge("plan", "research")

    workflow.add_conditional_edges(
        "research",
        route_after_research,
        {
            "summarize": "summarize",
            END: END
        }
    )

    workflow.add_edge("summarize", "write")
    workflow.add_edge("write", "critique")

    workflow.add_conditional_edges(
        "critique",
        route_after_critique,
        {
            "revise": "revise",
            "send_simulation": "send_simulation",
            END: END
        }
    )

    workflow.add_edge("revise", "critique")
    workflow.add_edge("send_simulation", END)

    return workflow.compile()

# Singleton compiled graph
newsletter_graph = build_newsletter_graph()

# In-memory runtime state store for runs
RUN_STATES: Dict[str, AgentState] = {}

def run_newsletter_agent(
    goal: str,
    mode: str = "autonomous",
    run_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Primary Entry Point Function.
    Executes the autonomous AI newsletter workflow.
    """
    state = create_initial_state(goal=goal, mode=mode, run_id=run_id)
    RUN_STATES[state["run_id"]] = state

    # Execute graph
    final_state = newsletter_graph.invoke(state)
    RUN_STATES[state["run_id"]] = final_state
    return final_state

def resume_after_research_approval(
    run_id: str,
    approved_articles: Optional[list] = None
) -> Dict[str, Any]:
    """Resumes execution from the research checkpoint in HITL mode."""
    state = RUN_STATES.get(run_id)
    if not state:
        raise ValueError(f"Run {run_id} not found")

    state["research_approved"] = True
    if approved_articles:
        state["selected_articles"] = approved_articles
    state["status"] = "summarizing"

    # Create sub-graph or invoke remaining nodes
    sub_workflow = StateGraph(AgentState)
    sub_workflow.add_node("summarize", summarize_node)
    sub_workflow.add_node("write", write_node)
    sub_workflow.add_node("critique", critique_node)
    sub_workflow.add_node("revise", revise_node)
    sub_workflow.add_node("send_simulation", send_simulation_node)

    sub_workflow.set_entry_point("summarize")
    sub_workflow.add_edge("summarize", "write")
    sub_workflow.add_edge("write", "critique")
    sub_workflow.add_conditional_edges(
        "critique",
        route_after_critique,
        {
            "revise": "revise",
            "send_simulation": "send_simulation",
            END: END
        }
    )
    sub_workflow.add_edge("revise", "critique")
    sub_workflow.add_edge("send_simulation", END)

    compiled_sub = sub_workflow.compile()
    final_state = compiled_sub.invoke(state)
    RUN_STATES[run_id] = final_state
    return final_state

def resume_after_newsletter_approval(
    run_id: str
) -> Dict[str, Any]:
    """Resumes execution from the newsletter approval checkpoint in HITL mode."""
    state = RUN_STATES.get(run_id)
    if not state:
        raise ValueError(f"Run {run_id} not found")

    state["newsletter_approved"] = True
    state["status"] = "sending"

    # Execute simulated sending node
    result_update = send_simulation_node(state)
    state.update(result_update)
    RUN_STATES[run_id] = state
    return state

def request_newsletter_revision(
    run_id: str,
    feedback: str
) -> Dict[str, Any]:
    """Requests revisions on the newsletter draft in HITL mode."""
    state = RUN_STATES.get(run_id)
    if not state:
        raise ValueError(f"Run {run_id} not found")

    state["revision_feedback"] = feedback
    state["status"] = "revising"

    # Revise and re-critique
    revise_res = revise_node(state)
    state.update(revise_res)
    critique_res = critique_node(state)
    state.update(critique_res)

    RUN_STATES[run_id] = state
    return state
