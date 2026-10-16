import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from backend.config import settings

def extract_json(text: str) -> Dict[str, Any]:
    """Clean markdown code fences and extract valid JSON."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text)
        text = re.sub(r"```$", "", text).strip()
    try:
        return json.loads(text)
    except Exception:
        # Fallback regex search for json object
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise ValueError(f"Could not parse valid JSON from text: {text[:200]}...")

class LLMService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model_name = settings.OPENAI_MODEL
        self.client = None
        if self.api_key and not settings.FORCE_DEMO:
            try:
                from langchain_openai import ChatOpenAI
                self.client = ChatOpenAI(
                    model=self.model_name,
                    api_key=self.api_key,
                    temperature=0.2
                )
            except Exception as e:
                print(f"Warning: Failed to initialize ChatOpenAI: {e}")
                self.client = None

    def invoke_prompt(self, system_prompt: str, user_prompt: str) -> str:
        """Call the OpenAI model via LangChain or fall back to demo synthesis."""
        if self.client:
            try:
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
                response = self.client.invoke(messages)
                return response.content
            except Exception as e:
                print(f"OpenAI API call failed: {e}. Falling back to demo generation.")

        # Fallback to realistic deterministic generator
        return self._demo_generate(system_prompt, user_prompt)

    def _demo_generate(self, system_prompt: str, user_prompt: str) -> str:
        """Realistic demo generation when API key is unavailable."""
        now_str = datetime.now().strftime("%B %d, %Y")
        
        # 1. Planning prompt handler
        if "Autonomous AI Research & Newsletter Planning Agent" in system_prompt:
            return json.dumps({
                "topic": "Autonomous AI Agents and Frontier Multi-Agent Systems",
                "audience": "AI Engineers, Enterprise Architects, and Tech Leaders",
                "time_range": "Past 7 days",
                "target_article_count": 6,
                "search_queries": [
                    "latest autonomous AI agent breakthroughs",
                    "SWE-bench coding agents production deployments",
                    "multi-agent orchestration frameworks LangGraph",
                    "security vulnerabilities and prompt injection AI agents"
                ],
                "execution_steps": [
                    "Step 1: Extract goal parameters and formulate targeted AI news queries",
                    "Step 2: Query search engine for top AI agent developments",
                    "Step 3: Deduplicate articles and validate canonical source links",
                    "Step 4: Select 6 high-impact stories and produce technical summaries",
                    "Step 5: Synthesize executive trends and generate responsive newsletter",
                    "Step 6: Execute multi-dimensional editorial critique and URL verification",
                    "Step 7: Finalize publication files and simulate subscriber broadcast"
                ]
            })

        # 2. Summarization prompt handler
        if "senior AI journalist and technical analyst" in system_prompt:
            # Parse articles from user prompt if available
            summaries = []
            try:
                data = json.loads(user_prompt)
                articles = data.get("articles", [])
            except Exception:
                articles = []

            for art in articles[:6]:
                title = art.get("title", "Autonomous Agent Breakthrough")
                source = art.get("source", "AI Research")
                url = art.get("url", "https://arxiv.org")
                snippet = art.get("snippet", "Major advances in autonomous decision making.")
                date = art.get("published_date", "Recent")
                
                summaries.append({
                    "title": title,
                    "source": source,
                    "published_date": date,
                    "summary": f"{snippet[:180]}... This development marks an acceleration in deploying self-directed agentic pipelines for mission-critical software and enterprise workflows.",
                    "why_it_matters": "Autonomous agents are shifting from speculative demos to hardened production systems capable of multi-step planning, automated recovery, and specialized tool synthesis.",
                    "key_takeaway": "Reliable execution loops and rigorous benchmark validation are now prioritized over raw model parameter scaling.",
                    "url": url
                })
            return json.dumps({"summaries": summaries})

        # 3. Newsletter Generation prompt handler
        if "award-winning technology newsletter editor-in-chief" in system_prompt:
            try:
                data = json.loads(user_prompt)
                summaries = data.get("summaries", [])
            except Exception:
                summaries = []

            article_count = len(summaries)
            subject = f"⚡ The Agentic Frontier: {article_count} Breakthroughs in Autonomous AI & Coding Agents"
            title = "The Agentic Frontier — Weekly Intelligence Dispatch"
            editors_note = (
                "Welcome to this week's edition of The Agentic Frontier. The paradigm shift from passive conversational "
                "models to proactive, agentic systems has crossed an inflection point. With computer use capabilities, "
                "hardened software engineering benchmarks, and multi-agent coordination architectures maturing rapidly, "
                "we examine the top developments redefining artificial intelligence this week."
            )
            trends = [
                "Tool-augmented agents are replacing monolithic single-turn LLM prompts across developer toolchains.",
                "SWE-bench Verified is establishing the ground truth standard for measuring real software engineering agent capabilities.",
                "Multi-agent state machines are superseding fragile linear chains, introducing robust human-in-the-loop checkpoints."
            ]
            closing = "Stay curious and keep orchestrating. The future belongs to those who build autonomous leverage."

            # Build Markdown
            md_lines = [
                f"# {title}",
                f"**Issue Date:** {now_str} | **Audience:** AI Engineers & Practitioners",
                "",
                "## 📝 Editor's Note",
                editors_note,
                "",
                "---",
                "## 🚀 Top Agentic AI Stories This Week",
                ""
            ]

            html_articles = []
            for idx, item in enumerate(summaries, 1):
                md_lines.extend([
                    f"### {idx}. [{item['title']}]({item['url']})",
                    f"*Source: {item['source']} | Date: {item.get('published_date', 'Recent')}*",
                    "",
                    f"**Summary:** {item['summary']}",
                    "",
                    f"**Why It Matters:** {item['why_it_matters']}",
                    "",
                    f"💡 **Key Takeaway:** {item['key_takeaway']}",
                    "",
                    f"🔗 [Read Full Article at {item['source']}]({item['url']})",
                    "",
                    "---"
                ])

                html_articles.append(f"""
                <div style="background-color: #1e293b; border-radius: 8px; padding: 20px; margin-bottom: 24px; border: 1px solid #334155;">
                  <h3 style="margin-top: 0; color: #38bdf8; font-size: 18px; line-height: 1.4;">
                    <a href="{item['url']}" style="color: #38bdf8; text-decoration: none;" target="_blank">{idx}. {item['title']}</a>
                  </h3>
                  <p style="color: #94a3b8; font-size: 13px; margin: 4px 0 12px 0;">
                    <strong>Source:</strong> {item['source']} &bull; <strong>Date:</strong> {item.get('published_date', 'Recent')}
                  </p>
                  <p style="color: #e2e8f0; font-size: 15px; line-height: 1.6; margin: 10px 0;">
                    {item['summary']}
                  </p>
                  <div style="background-color: #0f172a; border-left: 3px solid #6366f1; padding: 10px 14px; margin: 12px 0; border-radius: 4px;">
                    <strong style="color: #a5b4fc; font-size: 13px;">Why It Matters:</strong>
                    <p style="color: #cbd5e1; font-size: 14px; margin: 4px 0 0 0; line-height: 1.5;">{item['why_it_matters']}</p>
                  </div>
                  <p style="color: #fcd34d; font-size: 14px; font-weight: 500; margin: 10px 0;">
                    💡 <em>Takeaway:</em> {item['key_takeaway']}
                  </p>
                  <a href="{item['url']}" target="_blank" style="display: inline-block; margin-top: 10px; color: #60a5fa; font-size: 13px; text-decoration: underline;">
                    Read original source &rarr;
                  </a>
                </div>
                """)

            md_lines.extend([
                "## 🌐 Emerging Trends & Strategic Takeaways",
                ""
            ])
            for t in trends:
                md_lines.append(f"- **{t.split(':')[0]}**: {t}")

            md_lines.extend([
                "",
                "## 📨 Closing Dispatch",
                closing,
                "",
                f"*Simulated distribution generated autonomously by AI Newsletter Agent on {now_str}.*"
            ])

            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{subject}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #e2e8f0;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #0b0f19; padding: 30px 15px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" style="max-width: 680px; background-color: #111827; border-radius: 12px; border: 1px solid #1f2937; overflow: hidden; padding: 32px;">
          <tr>
            <td>
              <div style="display: inline-block; background-color: #312e81; color: #c7d2fe; font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 9999px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;">
                Autonomous Agent Edition
              </div>
              <h1 style="color: #ffffff; font-size: 26px; line-height: 1.3; margin: 0 0 8px 0;">
                {title}
              </h1>
              <p style="color: #94a3b8; font-size: 14px; margin: 0 0 24px 0;">
                Issue: {now_str} &bull; Curated for AI Engineers & Builders
              </p>
              
              <div style="background-color: #1e293b; border-left: 4px solid #38bdf8; padding: 16px; border-radius: 6px; margin-bottom: 30px;">
                <h4 style="margin: 0 0 6px 0; color: #38bdf8; font-size: 15px; text-transform: uppercase; letter-spacing: 0.04em;">Editor's Note</h4>
                <p style="color: #cbd5e1; font-size: 14px; line-height: 1.6; margin: 0;">
                  {editors_note}
                </p>
              </div>

              <h2 style="color: #f1f5f9; font-size: 20px; border-bottom: 1px solid #334155; padding-bottom: 8px; margin: 28px 0 20px 0;">
                🔥 Featured Intelligence ({article_count} Selected Articles)
              </h2>

              {''.join(html_articles)}

              <div style="background-color: #1e1b4b; border-radius: 8px; padding: 20px; margin-top: 32px; border: 1px solid #3730a3;">
                <h3 style="color: #a5b4fc; font-size: 17px; margin-top: 0;">⚡ Emerging Patterns & Key Takeaways</h3>
                <ul style="color: #cbd5e1; font-size: 14px; line-height: 1.7; padding-left: 20px; margin-bottom: 0;">
                  {''.join(f'<li><strong>{t}</strong></li>' for t in trends)}
                </ul>
              </div>

              <div style="text-align: center; margin-top: 36px; padding-top: 24px; border-top: 1px solid #1f2937; color: #64748b; font-size: 12px;">
                <p style="margin: 0 0 6px 0;">{closing}</p>
                <p style="margin: 0;">Generated by Autonomous AI Newsletter Agent &bull; Simulated Delivery</p>
              </div>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

            return json.dumps({
                "subject_line": subject,
                "newsletter_title": title,
                "editors_note": editors_note,
                "emerging_trends": trends,
                "closing": closing,
                "newsletter_markdown": "\n".join(md_lines),
                "newsletter_html": html_content
            })

        # 4. Critique prompt handler
        if "Senior AI Editorial Reviewer" in system_prompt:
            return json.dumps({
                "quality_score": 94,
                "is_valid": True,
                "issues": [],
                "suggestions": [
                    "Continue expanding technical details regarding benchmark performance in future editions.",
                    "Include benchmark latency metrics when discussing edge model execution."
                ]
            })

        # 5. Revision prompt handler
        if "expert AI Newsletter Editor tasked with revising" in system_prompt:
            return json.dumps({
                "subject_line": "⚡ Revised: Frontier AI Agent Weekly Dispatch",
                "newsletter_title": "The Agentic Frontier — Polished Edition",
                "newsletter_markdown": user_prompt,
                "newsletter_html": "<div>Revised Newsletter Content</div>"
            })

        return json.dumps({"status": "acknowledged", "timestamp": now_str})

llm_service = LLMService()
