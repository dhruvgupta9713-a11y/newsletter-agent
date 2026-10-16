import pytest
from backend.services.search_service import is_valid_url, deduplicate_articles
from backend.agent.tools import (
    search_ai_news,
    summarize_articles,
    generate_newsletter,
    critique_newsletter,
    simulate_send_newsletter
)

def test_url_validation():
    assert is_valid_url("https://techcrunch.com/article/ai-agents") is True
    assert is_valid_url("http://openai.com/blog") is True
    assert is_valid_url("not-a-url") is False
    assert is_valid_url("ftp://example.com") is False
    assert is_valid_url("") is False
    assert is_valid_url(None) is False

def test_search_deduplication():
    raw = [
        {"title": "OpenAI Launches SWE-bench", "url": "https://openai.com/swe", "source": "OpenAI"},
        {"title": "OpenAI Launches SWE-bench", "url": "https://openai.com/swe/", "source": "OpenAI"},
        {"title": "Different Article", "url": "https://techcrunch.com/diff", "source": "TechCrunch"},
        {"title": "Invalid Url Article", "url": "not-valid", "source": "Bad"}
    ]
    deduped = deduplicate_articles(raw)
    assert len(deduped) == 2
    assert deduped[0]["url"] == "https://openai.com/swe"
    assert deduped[1]["url"] == "https://techcrunch.com/diff"

def test_search_ai_news_tool():
    res = search_ai_news("autonomous coding agents", max_results=5)
    assert "articles" in res
    assert len(res["articles"]) >= 1
    assert "query" in res
    assert "provider" in res

def test_summarize_articles_tool():
    sample_articles = [
        {
            "title": f"Article {i}",
            "url": f"https://example.com/art-{i}",
            "source": "TechNews",
            "snippet": f"Snippet for article {i}",
            "published_date": "Recent"
        }
        for i in range(5)
    ]
    summaries = summarize_articles(sample_articles)
    assert len(summaries) == 5
    for s in summaries:
        assert "title" in s
        assert "why_it_matters" in s
        assert "key_takeaway" in s
        assert is_valid_url(s["url"])

def test_critique_deterministic_checks():
    summaries = [
        {"title": f"Article {i}", "url": f"https://example.com/{i}"}
        for i in range(6)
    ]
    newsletter_good = {
        "subject_line": "⚡ Breaking Agent News",
        "newsletter_html": "<html>" + "x" * 200 + "</html>",
        "newsletter_markdown": "# Title\n" + "x" * 200
    }
    critique = critique_newsletter(newsletter_good, summaries, "Cover AI agents")
    assert critique["quality_score"] >= 80
    assert critique["deterministic_checks"]["article_count_valid"] is True
    assert critique["deterministic_checks"]["all_urls_valid"] is True

    # Test failure with too few articles
    few_summaries = summaries[:3]
    bad_critique = critique_newsletter(newsletter_good, few_summaries, "Cover AI agents")
    assert bad_critique["deterministic_checks"]["article_count_valid"] is False
    assert any("Expected 5 to 7 articles" in issue for issue in bad_critique["issues"])

def test_simulate_send_newsletter():
    newsletter_data = {
        "subject_line": "Simulated Newsletter Subject",
        "newsletter_html": "<html><body>Hello Subscribers</body></html>",
        "newsletter_markdown": "# Hello Subscribers"
    }
    result = simulate_send_newsletter(newsletter_data, run_id="test_run_123")
    delivery = result["delivery"]
    assert delivery["simulated"] is True
    assert delivery["status"] == "DELIVERED_SIMULATED"
    assert delivery["recipient_count"] > 0
    assert "saved_files" in result
    assert "html_path" in result["saved_files"]
    assert "md_path" in result["saved_files"]
    assert "json_path" in result["saved_files"]
