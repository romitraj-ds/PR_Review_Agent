import os
import sys
import traceback
from typing import Any, Dict
from mcp.server.fastmcp import FastMCP

from dotenv import load_dotenv

from github_integration import fetch_pr_changes, post_github_pr_comment
from review_formatter import format_review


class PRAnalyzer:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        print(f"Environment variables loaded, {os.getenv('GOOGLE_API_KEY')}, {os.getenv('GITHUB_TOKEN')}" )

        # Initialize MCP Server
        self.mcp = FastMCP("github_pr_analysis")
        print("MCP Server initialized", file=sys.stderr)

        # Register MCP tools
        self._register_tools()


    def _register_tools(self):
        """Register MCP tools for PR analysis."""

        @self.mcp.tool()
        async def fetch_pr(repo_owner: str, repo_name: str, pr_number: int) -> Dict[str, Any]:
            """Fetch changes from a GitHub pull request."""
            print(f"Fetching PR #{pr_number} from {repo_owner}/{repo_name}", file=sys.stderr)
            try:
                pr_info = fetch_pr_changes(repo_owner, repo_name, pr_number)
                if pr_info is None:
                    print("No changes returned from fetch_pr_changes", file=sys.stderr)
                    return {}
                print(f"Successfully fetched PR information", file=sys.stderr)
                return pr_info
            except Exception as e:
                print(f"Error fetching PR: {str(e)}", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                return {}

        @self.mcp.tool()
        async def comment_on_pr(repo_owner: str, repo_name: str, pr_number: int, analysis: str) -> str:
            """Post a comment on a GitHub pull request."""
            print(f"Posting comment on PR #{pr_number} in {repo_owner}/{repo_name}", file=sys.stderr)
            try:
                pr_info = fetch_pr_changes(repo_owner, repo_name, pr_number)
                comment_body = format_review(pr_info, analysis)
                post_github_pr_comment(repo_owner, repo_name, pr_number, comment_body)
                return "Comment posted"
            except Exception as e:
                return f"Failed to post comment: {str(e)}"

    def run(self):
        """Start the MCP server."""
        try:
            print("Running MCP Server for GitHub PR Analysis...", file=sys.stderr)
            self.mcp.run(transport="stdio")
        except Exception as e:
            print(f"Fatal Error in MCP Server: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    analyzer = PRAnalyzer()
    analyzer.run()