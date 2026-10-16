from typing import List, Dict, Any

# Realistic curated AI agent articles for demo mode or search fallback
DEMO_ARTICLES: List[Dict[str, Any]] = [
    {
        "title": "Anthropic Introduces Computer Use and Autonomous Multi-Agent Desktop Workflows",
        "url": "https://www.anthropic.com/news/3-5-models-and-computer-use",
        "source": "Anthropic Research",
        "published_date": "October 2024",
        "snippet": "Anthropic has upgraded Claude 3.5 Sonnet to include direct computer use capabilities, enabling the model to look at a screen, move a cursor, click buttons, and type text to complete complex multi-step developer and administrative workflows autonomously.",
    },
    {
        "title": "SWE-bench Verified: Standardizing Benchmark Protocols for Autonomous AI Software Engineers",
        "url": "https://openai.com/index/introducing-swe-bench-verified",
        "source": "OpenAI / SWE-bench",
        "published_date": "August 2024",
        "snippet": "OpenAI and the SWE-bench team unveiled SWE-bench Verified, a curated subset of 500 human-validated software engineering tasks to accurately benchmark autonomous AI coding agents resolving GitHub issues.",
    },
    {
        "title": "LangGraph: Multi-Agent Orchestration Framework Scales for Production Systems",
        "url": "https://blog.langchain.com/langgraph-multi-agent-workflows",
        "source": "LangChain Blog",
        "published_date": "September 2024",
        "snippet": "LangGraph provides cyclically connected state machines enabling developer teams to orchestrate multi-agent collaboration with human-in-the-loop checkpoints, persistent memory states, and streaming execution.",
    },
    {
        "title": "AutoGPT 2.0 and the Evolution of Autonomous Task Planning Architectures",
        "url": "https://venturebeat.com/ai/the-evolution-of-autonomous-ai-agents-in-enterprise",
        "source": "VentureBeat",
        "published_date": "September 2024",
        "snippet": "Enterprise adoption of autonomous agent frameworks has surged by 230% in 2024. Next-generation systems move beyond simple linear chains to graph-based agent topologies with dynamic replanning and tool sandboxes.",
    },
    {
        "title": "Meta Releases Llama 3.2 with Lightweight Vision Models Built for Edge Agents",
        "url": "https://ai.meta.com/blog/llama-3-2-connect-2024",
        "source": "Meta AI",
        "published_date": "September 2024",
        "snippet": "Meta announced Llama 3.2, offering 1B and 3B parameter models optimized for on-device agentic execution and multimodal 11B/90B models designed to power autonomous agents across mobile and edge hardware.",
    },
    {
        "title": "Agentic AI in Healthcare: Stanford Medicine Tests Multi-Agent Clinical Trials Matching",
        "url": "https://www.technologyreview.com/2024/09/18/ai-agents-clinical-trials-medicine",
        "source": "MIT Technology Review",
        "published_date": "September 2024",
        "snippet": "Researchers at Stanford tested collaborative multi-agent LLM systems that digest complex clinical protocols, analyze patient health records, and match patients to ongoing oncology trials with 94% precision.",
    },
    {
        "title": "Google DeepMind Unveils Autonomous Code Synthesis and Verification Framework",
        "url": "https://deepmind.google/discover/blog/alphacode-2-advances-competitive-programming",
        "source": "Google DeepMind",
        "published_date": "October 2024",
        "snippet": "DeepMind demonstrated autonomous agent verification loops where code generating models partner with automated test-case generators and formal verification provers to achieve superhuman competitive programming results.",
    },
    {
        "title": "Security in the Age of Agentic AI: Mitigating Prompt Injections in Tool Calling",
        "url": "https://techcrunch.com/2024/10/02/securing-autonomous-ai-agents-from-indirect-injections",
        "source": "TechCrunch",
        "published_date": "October 2024",
        "snippet": "As autonomous agents gain terminal and browser access, cybersecurity researchers demonstrate novel defenses against indirect prompt injections hidden inside external websites and API payloads.",
    },
    {
        "title": "Hugging Face Launches Smolagents: Lightweight Code Agents in Pure Python",
        "url": "https://huggingface.co/blog/smolagents",
        "source": "Hugging Face",
        "published_date": "November 2024",
        "snippet": "Smolagents brings a minimalist approach to agent architectures, letting LLMs write Python code snippets directly to interact with tools rather than clumsy JSON schemas, dramatically reducing latency and errors.",
    }
]

# Configurable sample subscriber list for simulated delivery
DEMO_SUBSCRIBERS: List[str] = [
    "sarah.connor@ai-ventures.io",
    "marcus.vance@techfrontier.dev",
    "elena.rostova@deepagents.org",
    "chen.wei@automata-labs.com",
    "david.miller@enterprise-ml.net",
    "priya.sharma@horizon-ai.tech",
    "alex.thorne@quantum-compute.co",
    "sophia.martinez@agentic-systems.io",
    "nathan.brooks@synthetic-intelligence.ai",
    "olivia.taylor@llm-newsletter.com"
]
