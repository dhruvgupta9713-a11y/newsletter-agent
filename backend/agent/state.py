from typing import TypedDict, List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ArticleItem(BaseModel):
    title: str
    url: str
    source: str
    snippet: str = ""
    published_date: Optional[str] = "Recent"
    score: Optional[float] = None
    approved: bool = True

class ArticleSummary(BaseModel):
    title: str
    source: str
    published_date: str = "Recent"
    summary: str
    why_it_matters: str
    key_takeaway: str
    url: str

class PlanData(BaseModel):
    topic: str
    audience: str
    time_range: str
    target_article_count: int = 5
    execution_steps: List[str] = Field(default_factory=list)

class CritiqueResult(BaseModel):
    quality_score: int
    is_valid: bool
    issues: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    deterministic_checks: Dict[str, Any] = Field(default_factory=dict)

class DeliveryResult(BaseModel):
    simulated: bool = True
    recipient_count: int
    timestamp: str
    status: str = "DELIVERED_SIMULATED"
    subscribers_sample: List[str] = Field(default_factory=list)
    note: str = "SIMULATED: No actual emails were transmitted."

class ActivityLogEntry(BaseModel):
    timestamp: str
    step: str
    tool_name: str
    description: str
    status: str = "success"  # "success", "warning", "error", "running"
    details: Optional[Dict[str, Any]] = None

class AgentState(TypedDict):
    run_id: str
    goal: str
    mode: str  # "autonomous" or "hitl"
    plan: Optional[Dict[str, Any]]
    search_queries: List[str]
    raw_articles: List[Dict[str, Any]]
    selected_articles: List[Dict[str, Any]]
    research_approved: bool
    summaries: List[Dict[str, Any]]
    newsletter_title: str
    subject_line: str
    newsletter_html: str
    newsletter_markdown: str
    newsletter_approved: bool
    critique: Optional[Dict[str, Any]]
    revision_count: int
    revision_feedback: Optional[str]
    simulated_delivery: Optional[Dict[str, Any]]
    output_files: Dict[str, str]
    logs: List[Dict[str, Any]]
    current_step: str
    status: str  # "planning", "researching", "waiting_research_approval", "summarizing", "writing", "critiquing", "revising", "waiting_newsletter_approval", "sending", "completed", "failed", "rejected"
    error: Optional[str]
    start_time: float
    duration_seconds: float
