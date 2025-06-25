def format_review(pr_info: dict, analysis: str) -> str:
    """
    Formats pull request metadata and file changes into a markdown string suitable
    for posting as a GitHub comment.

    Args:
        pr_info (dict): Dictionary containing PR metadata and file changes.
        analysis (str): LLM-generated textual review.

    Returns:
        str: A markdown-formatted summary of the PR.
    """
    if not pr_info:
        return "❌ No PR information available."

    top_changes = "\n".join(
        f"- `{c['filename']}` ({c['status']}, +{c['additions']}/-{c['deletions']})"
        for c in pr_info.get('changes', [])[:5]  # limit to top 5
    )

    return f"""### 🤖 Automated Pull Request Review

**Title**: {pr_info.get('title', 'N/A')}
**Author**: 'PR Reviewer'
**Files Changed**: {pr_info.get('total_changes', 0)}

#### 📄 Top File Changes:
{top_changes}

---

#### 🧠 Analysis:
{analysis.strip()}

---

_This review was generated automatically by an AI-based reviewer._
"""
