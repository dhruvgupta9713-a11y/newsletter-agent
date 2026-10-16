#!/usr/bin/env python3
"""
CLI entry point and standalone runner for the AI Newsletter Agent.
Enables running the entire workflow via:
  from run_newsletter_agent import run_newsletter_agent
  state = run_newsletter_agent(goal="...", mode="autonomous")
Or directly from the command line:
  python run_newsletter_agent.py --goal "..." --mode autonomous
"""

import sys
import argparse
import json
from pathlib import Path

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.agent.graph import run_newsletter_agent

def main():
    parser = argparse.ArgumentParser(description="Autonomous AI Newsletter Agent Runner")
    parser.add_argument(
        "--goal",
        type=str,
        default="Create a weekly newsletter on the latest AI agent news and send it to our subscribers.",
        help="Natural language newsletter objective"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["autonomous", "hitl"],
        default="autonomous",
        help="Execution mode: 'autonomous' or 'hitl'"
    )
    args = parser.parse_args()

    print(f"\n=======================================================")
    print(f"🚀 Launching AI Newsletter Agent")
    print(f"   Goal: {args.goal}")
    print(f"   Mode: {args.mode}")
    print(f"=======================================================\n")

    result = run_newsletter_agent(goal=args.goal, mode=args.mode)

    print("\n---------------- Execution Summary ----------------")
    print(f"Run ID:            {result.get('run_id')}")
    print(f"Status:            {result.get('status')}")
    print(f"Selected Articles: {len(result.get('selected_articles', []))}")
    print(f"Critique Score:    {result.get('critique', {}).get('quality_score')}/100")
    print(f"Revisions Made:    {result.get('revision_count', 0)}")
    print(f"Duration:          {result.get('duration_seconds', 0)}s")
    
    if result.get("simulated_delivery"):
        deliv = result["simulated_delivery"]
        print(f"Simulated Send:    {deliv.get('status')} to {deliv.get('recipient_count')} recipients")

    output_files = result.get("output_files", {})
    if output_files:
        print("\nSaved Output Files:")
        print(f"  - HTML:     {output_files.get('html_path')}")
        print(f"  - Markdown: {output_files.get('md_path')}")
        print(f"  - Report:   {output_files.get('json_path')}")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
