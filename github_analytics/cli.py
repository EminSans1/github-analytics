"""CLI interface for GitHub Analytics."""

import argparse
import sys

from .analyzer import GitHubAnalyzer
from .github_api import GitHubAPI
from .reporter import Reporter
from .visualizer import Visualizer


def main():
    parser = argparse.ArgumentParser(
        description="GitHub Analytics CLI - Analyze GitHub profiles and repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  github-analytics user EminSans1
  github-analytics user EminSans1 --detailed
  github-analytics user EminSans1 --export report.md
  github-analytics repo EminSans1/system-monitor
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    user_parser = subparsers.add_parser("user", help="Analyze a GitHub user")
    user_parser.add_argument("username", help="GitHub username to analyze")
    user_parser.add_argument("--detailed", "-d", action="store_true", help="Show detailed analysis")
    user_parser.add_argument("--export", "-e", help="Export report to Markdown file")

    repo_parser = subparsers.add_parser("repo", help="Analyze a GitHub repository")
    repo_parser.add_argument("repository", help="Repository in format owner/repo")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    api = GitHubAPI()
    analyzer = GitHubAnalyzer(api)
    visualizer = Visualizer()
    reporter = Reporter()

    try:
        if args.command == "user":
            analysis = analyzer.analyze_user(args.username, detailed=args.detailed)
            visualizer.display_profile(analysis, detailed=args.detailed)

            if args.export:
                report = reporter.generate_markdown(analysis)
                with open(args.export, "w", encoding="utf-8") as f:
                    f.write(report)
                visualizer.console.print(f"\n[green]Report exported to {args.export}[/green]")

        elif args.command == "repo":
            owner, repo = args.repository.split("/")
            visualizer.console.print(f"[bold]Analyzing repository: {owner}/{repo}[/bold]")
            visualizer.console.print("[yellow]Repository analysis coming soon![/yellow]")

    except Exception as e:
        visualizer.display_error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()