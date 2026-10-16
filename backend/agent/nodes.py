import time
from datetime import datetime
from typing import Dict, Any, List
from backend.agent.state import AgentState, ActivityLogEntry
from backend.agent.tools import (
    search_ai_news,
    summarize_articles,
    generate_newsletter,
    critique_newsletter,
    revise_newsletter,
    simulate_send_newsletter
)
from backend.agent.prompts import PLANNING_SYSTEM_PROMPT
from backend.services.llm_service import llm_service, extract_json
from backend.services.search_service import deduplicate_articles

def create_log_entry(step: str, tool_name: str, description: str, status: str = "success", details: Dict[str, Any] = None) -> Dict[str, Any]:
    return {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "step": step,
        "tool_name": tool_name,
        "description": description,
        "status": status,
        "details": details or {}
    }

def plan_node(state: AgentState) -> Dict[str, Any]:
    """Step 1: Goal Understanding and Planning."""
    goal = state.get("goal", "")
    state_logs = list(state.get("logs", []))

    plan_response = llm_service.invoke_prompt(
        system_prompt=PLANNING_SYSTEM_PROMPT,
        user_prompt=f"Goal: {goal}"
    )

    try:
        plan_data = extract_json(plan_response)
    except Exception as e:
        plan_data = {
            "topic": "Autonomous AI Agents & Multi-Agent Systems",
            "audience": "AI Engineers and Tech Enthusiasts",
            "time_range": "Recent",
            "target_article_count": 6,
            "search_queries": [
                "autonomous AI agents breakthrough news",
                "SWE-bench verified AI coding agents",
                "multi-agent orchestration systems production"
            ],
            "execution_steps": [
                "Understand goal and plan research queries",
                "Execute search across AI news sources",
                "Deduplicate and select top 5-7 articles",
                "Generate analytical summaries with key takeaways",
                "Draft responsive newsletter HTML & Markdown",
                "Perform editorial self-critique and URL validation",
                "Simulate distribution to subscribers"
            ]
        }

    queries = plan_data.get("search_queries", ["AI agents news", "autonomous coding agents"])
    
    log_entry = create_log_entry(
        step="Planning",
        tool_name="extract_execution_plan",
        description=f"Formulated research plan for '{plan_data.get('topic')}' with {len(queries)} search queries.",
        details={"plan": plan_data}
    )
    state_logs.append(log_entry)

    return {
        "plan": plan_data,
        "search_queries": queries,
        "current_step": "planning",
        "status": "researching",
        "logs": state_logs
    }

def research_node(state: AgentState) -> Dict[str, Any]:
    """Step 2: Research Tool & Article Gathering."""
    queries = state.get("search_queries", [])
    state_logs = list(state.get("logs", []))
    all_raw_articles = []
    providers_used = set()
    is_demo_active = False

    for q in queries:
        search_res = search_ai_news(q, max_results=5)
        articles = search_res.get("articles", [])
        all_raw_articles.extend(articles)
        providers_used.add(search_res.get("provider", "Search"))
        if search_res.get("is_demo_mode"):
            is_demo_active = True

    # Deduplicate across all query results
    deduped = deduplicate_articles(all_raw_articles)
    
    # Target 5-7 articles
    target_count = state.get("plan", {}).get("target_article_count", 6)
    target_count = max(5, min(7, target_count))
    selected = deduped[:target_count]

    log_entry = create_log_entry(
        step="Researching",
        tool_name="search_ai_news",
        description=f"Retrieved {len(deduped)} unique articles using {', '.join(providers_used)}. Selected {len(selected)} articles.",
        details={
            "total_found": len(deduped),
            "selected_count": len(selected),
            "providers": list(providers_used),
            "demo_mode": is_demo_active
        }
    )
    state_logs.append(log_entry)

    # Determine next status based on mode
    mode = state.get("mode", "autonomous")
    research_approved = state.get("research_approved", False)

    if mode == "hitl" and not research_approved:
        next_status = "waiting_research_approval"
    else:
        next_status = "summarizing"

    return {
        "raw_articles": deduped,
        "selected_articles": selected,
        "current_step": "researching",
        "status": next_status,
        "logs": state_logs
    }

def summarize_node(state: AgentState) -> Dict[str, Any]:
    """Step 3: Article Selection and Summarization."""
    selected = state.get("selected_articles", [])
    state_logs = list(state.get("logs", []))

    # Keep only approved articles if user filtered in HITL
    approved_articles = [a for a in selected if a.get("approved", True)]
    if len(approved_articles) < 5:
        # Fall back to using selected articles to ensure 5-7 count
        approved_articles = selected[:6]

    summaries = summarize_articles(approved_articles)

    log_entry = create_log_entry(
        step="Summarizing",
        tool_name="summarize_articles",
        description=f"Analyzed and synthesized technical summaries for {len(summaries)} articles with key takeaways.",
        details={"summaries_count": len(summaries)}
    )
    state_logs.append(log_entry)

    return {
        "summaries": summaries,
        "current_step": "summarizing",
        "status": "writing",
        "logs": state_logs
    }

def write_node(state: AgentState) -> Dict[str, Any]:
    """Step 4: Newsletter Generation."""
    summaries = state.get("summaries", [])
    goal = state.get("goal", "")
    plan = state.get("plan", {})
    state_logs = list(state.get("logs", []))

    newsletter = generate_newsletter(summaries=summaries, goal=goal, plan=plan)

    subject = newsletter.get("subject_line", "⚡ The Agentic Frontier: Weekly AI Agent Dispatch")
    title = newsletter.get("newsletter_title", "The Agentic Frontier")
    html_content = newsletter.get("newsletter_html", "")
    md_content = newsletter.get("newsletter_markdown", "")

    log_entry = create_log_entry(
        step="Writing",
        tool_name="generate_newsletter",
        description=f"Composed responsive HTML email and Markdown edition with subject: '{subject}'.",
        details={
            "subject": subject,
            "title": title,
            "html_length": len(html_content),
            "md_length": len(md_content)
        }
    )
    state_logs.append(log_entry)

    return {
        "subject_line": subject,
        "newsletter_title": title,
        "newsletter_html": html_content,
        "newsletter_markdown": md_content,
        "current_step": "writing",
        "status": "critiquing",
        "logs": state_logs
    }

def critique_node(state: AgentState) -> Dict[str, Any]:
    """Step 5: Self-Critique and Review."""
    summaries = state.get("summaries", [])
    goal = state.get("goal", "")
    newsletter_data = {
        "subject_line": state.get("subject_line"),
        "newsletter_title": state.get("newsletter_title"),
        "newsletter_html": state.get("newsletter_html"),
        "newsletter_markdown": state.get("newsletter_markdown")
    }
    state_logs = list(state.get("logs", []))

    critique_res = critique_newsletter(
        newsletter_data=newsletter_data,
        summaries=summaries,
        goal=goal
    )

    quality_score = critique_res.get("quality_score", 90)
    issues = critique_res.get("issues", [])
    is_valid = critique_res.get("is_valid", True)
    revision_count = state.get("revision_count", 0)

    log_entry = create_log_entry(
        step="Self-Critique",
        tool_name="critique_newsletter",
        description=f"Evaluated output: Quality Score {quality_score}/100. Issues detected: {len(issues)}.",
        status="success" if is_valid else "warning",
        details=critique_res
    )
    state_logs.append(log_entry)

    # Determine next routing
    mode = state.get("mode", "autonomous")
    newsletter_approved = state.get("newsletter_approved", False)

    if not is_valid and revision_count < 2:
        next_status = "revising"
    elif mode == "hitl" and not newsletter_approved:
        next_status = "waiting_newsletter_approval"
    else:
        next_status = "sending"

    return {
        "critique": critique_res,
        "current_step": "self_review",
        "status": next_status,
        "logs": state_logs
    }

def revise_node(state: AgentState) -> Dict[str, Any]:
    """Step 5b: Automated Revision Loop."""
    newsletter_data = {
        "subject_line": state.get("subject_line"),
        "newsletter_title": state.get("newsletter_title"),
        "newsletter_html": state.get("newsletter_html"),
        "newsletter_markdown": state.get("newsletter_markdown")
    }
    critique_data = state.get("critique", {})
    summaries = state.get("summaries", [])
    state_logs = list(state.get("logs", []))
    rev_count = state.get("revision_count", 0) + 1

    # Check for human feedback override
    if state.get("revision_feedback"):
        critique_data["issues"].append(f"Human Feedback: {state.get('revision_feedback')}")

    revised_data = revise_newsletter(
        newsletter_data=newsletter_data,
        critique_data=critique_data,
        summaries=summaries
    )

    log_entry = create_log_entry(
        step="Revising",
        tool_name="revise_newsletter",
        description=f"Applied editorial revisions (Attempt {rev_count}/2) to fix identified flaws.",
        details={"revision_attempt": rev_count}
    )
    state_logs.append(log_entry)

    return {
        "subject_line": revised_data.get("subject_line", state.get("subject_line")),
        "newsletter_title": revised_data.get("newsletter_title", state.get("newsletter_title")),
        "newsletter_html": revised_data.get("newsletter_html", state.get("newsletter_html")),
        "newsletter_markdown": revised_data.get("newsletter_markdown", state.get("newsletter_markdown")),
        "revision_count": rev_count,
        "revision_feedback": None,  # clear feedback once applied
        "current_step": "revising",
        "status": "critiquing",
        "logs": state_logs
    }

def send_simulation_node(state: AgentState) -> Dict[str, Any]:
    """Step 6: Output and Simulated Sending."""
    newsletter_data = {
        "subject_line": state.get("subject_line"),
        "newsletter_title": state.get("newsletter_title"),
        "newsletter_html": state.get("newsletter_html"),
        "newsletter_markdown": state.get("newsletter_markdown")
    }
    run_id = state.get("run_id", "run_default")
    state_logs = list(state.get("logs", []))

    sim_result = simulate_send_newsletter(
        newsletter_data=newsletter_data,
        run_id=run_id
    )

    delivery_info = sim_result["delivery"]
    saved_files = sim_result["saved_files"]

    start_time = state.get("start_time", time.time())
    duration = round(time.time() - start_time, 2)

    log_entry = create_log_entry(
        step="Simulated Sending",
        tool_name="simulate_send_newsletter",
        description=f"Simulated distribution to {delivery_info['recipient_count']} subscribers. Saved HTML, Markdown, and JSON files.",
        details={
            "delivery": delivery_info,
            "files": saved_files,
            "duration_seconds": duration
        }
    )
    state_logs.append(log_entry)

    return {
        "simulated_delivery": delivery_info,
        "output_files": saved_files,
        "current_step": "completed",
        "status": "completed",
        "duration_seconds": duration,
        "logs": state_logs
    }
