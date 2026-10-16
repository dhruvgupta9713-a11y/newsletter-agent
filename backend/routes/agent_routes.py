import json
import asyncio
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks, Response
from fastapi.responses import StreamingResponse, PlainTextResponse, HTMLResponse
from pydantic import BaseModel, Field
import uuid

from backend.agent.graph import (
    run_newsletter_agent,
    resume_after_research_approval,
    resume_after_newsletter_approval,
    request_newsletter_revision,
    RUN_STATES
)
from backend.services.storage_service import storage_service
from backend.config import get_system_status

router = APIRouter(prefix="/api/agent", tags=["Agent"])

class RunAgentRequest(BaseModel):
    goal: str = Field(..., description="Natural language newsletter objective")
    mode: str = Field("autonomous", description="'autonomous' or 'hitl'")
    topic: Optional[str] = None
    target_article_count: Optional[int] = 6

class ApproveResearchRequest(BaseModel):
    approved_articles: Optional[List[Dict[str, Any]]] = None

class ReviseNewsletterRequest(BaseModel):
    feedback: str = Field(..., description="Editorial instructions for revision")

@router.get("/status")
def get_status() -> Dict[str, Any]:
    """Returns LLM and search provider health/demo status."""
    return get_system_status()

@router.post("/run")
async def start_agent_workflow(
    req: RunAgentRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Initiates the autonomous or HITL AI newsletter agent workflow.
    """
    if not req.goal.strip():
        raise HTTPException(status_code=400, detail="Goal cannot be empty.")

    run_id = f"run_{uuid.uuid4().hex[:8]}"

    # If autonomous or HITL, we execute the graph.
    # Running in thread pool so it doesn't block async event loop
    loop = asyncio.get_event_loop()
    
    try:
        # Run agent
        result = await loop.run_in_executor(
            None,
            lambda: run_newsletter_agent(goal=req.goal, mode=req.mode, run_id=run_id)
        )
        return {
            "run_id": run_id,
            "status": result.get("status"),
            "current_step": result.get("current_step"),
            "state": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution error: {str(e)}")

@router.get("/{run_id}")
def get_agent_state(run_id: str) -> Dict[str, Any]:
    """Retrieves the full runtime state and history for a given run."""
    state = RUN_STATES.get(run_id)
    if not state:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found.")
    return state

@router.get("/{run_id}/events")
async def stream_agent_events(run_id: str):
    """
    Server-Sent Events (SSE) stream providing real-time workflow log updates.
    """
    state = RUN_STATES.get(run_id)
    if not state:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found.")

    async def event_generator():
        last_log_count = 0
        max_checks = 60
        check = 0

        while check < max_checks:
            curr_state = RUN_STATES.get(run_id)
            if not curr_state:
                break
            
            logs = curr_state.get("logs", [])
            if len(logs) > last_log_count:
                new_logs = logs[last_log_count:]
                last_log_count = len(logs)
                for entry in new_logs:
                    data = {
                        "run_id": run_id,
                        "status": curr_state.get("status"),
                        "current_step": curr_state.get("current_step"),
                        "log": entry
                    }
                    yield f"data: {json.dumps(data)}\n\n"

            if curr_state.get("status") in ("completed", "waiting_research_approval", "waiting_newsletter_approval", "failed"):
                # Final state event
                summary_data = {
                    "run_id": run_id,
                    "status": curr_state.get("status"),
                    "current_step": curr_state.get("current_step"),
                    "done": True
                }
                yield f"data: {json.dumps(summary_data)}\n\n"
                break

            await asyncio.sleep(0.5)
            check += 1

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.post("/{run_id}/approve-research")
async def approve_research(run_id: str, req: ApproveResearchRequest) -> Dict[str, Any]:
    """Approves selected articles and resumes the workflow in HITL mode."""
    if run_id not in RUN_STATES:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found.")
    
    loop = asyncio.get_event_loop()
    try:
        updated_state = await loop.run_in_executor(
            None,
            lambda: resume_after_research_approval(run_id=run_id, approved_articles=req.approved_articles)
        )
        return {
            "run_id": run_id,
            "status": updated_state.get("status"),
            "state": updated_state
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{run_id}/approve-newsletter")
async def approve_newsletter(run_id: str) -> Dict[str, Any]:
    """Approves the generated newsletter draft and proceeds to simulated sending in HITL mode."""
    if run_id not in RUN_STATES:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found.")
    
    loop = asyncio.get_event_loop()
    try:
        updated_state = await loop.run_in_executor(
            None,
            lambda: resume_after_newsletter_approval(run_id=run_id)
        )
        return {
            "run_id": run_id,
            "status": updated_state.get("status"),
            "state": updated_state
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{run_id}/revise")
async def revise_newsletter_endpoint(run_id: str, req: ReviseNewsletterRequest) -> Dict[str, Any]:
    """Submits human revision instructions and regenerates the newsletter draft in HITL mode."""
    if run_id not in RUN_STATES:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found.")
    
    loop = asyncio.get_event_loop()
    try:
        updated_state = await loop.run_in_executor(
            None,
            lambda: request_newsletter_revision(run_id=run_id, feedback=req.feedback)
        )
        return {
            "run_id": run_id,
            "status": updated_state.get("status"),
            "state": updated_state
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{run_id}/download/{format}")
def download_newsletter_file(run_id: str, format: str):
    """
    Downloads generated HTML, Markdown, or JSON execution report.
    Format: 'html', 'md', or 'json'
    """
    state = RUN_STATES.get(run_id)
    if not state:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found.")

    output_files = state.get("output_files", {})
    format_lower = format.lower()

    if format_lower == "html":
        content = state.get("newsletter_html", "")
        filename = output_files.get("html_filename", f"newsletter_{run_id}.html")
        return Response(
            content=content,
            media_type="text/html",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    elif format_lower in ("md", "markdown"):
        content = state.get("newsletter_markdown", "")
        filename = output_files.get("md_filename", f"newsletter_{run_id}.md")
        return Response(
            content=content,
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    elif format_lower in ("json", "report"):
        report_data = {
            "run_id": run_id,
            "goal": state.get("goal"),
            "plan": state.get("plan"),
            "critique": state.get("critique"),
            "simulated_delivery": state.get("simulated_delivery"),
            "duration_seconds": state.get("duration_seconds"),
            "logs": state.get("logs")
        }
        filename = output_files.get("json_filename", f"report_{run_id}.json")
        return Response(
            content=json.dumps(report_data, indent=2),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid format. Supported: 'html', 'md', 'json'.")
