"""Terminal visualization for GitHub analytics data."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .analyzer import ProfileAnalysis


class Visualizer:
    def __init__(self):
        self.console = Console()

    def display_profile(self, analysis: ProfileAnalysis, detailed: bool = False):
        self._display_header(analysis)
        self._display_profile_info(analysis)
        self._display_repo_stats(analysis)
        if detailed and analysis.languages:
            self._display_languages(analysis)
        self._display_scores(analysis)
        if analysis.recommendations:
            self._display_recommendations(analysis)

    def _display_header(self, analysis: ProfileAnalysis):
        title = f"GitHub Profile Analysis: {analysis.profile.username}"
        self.console.print(Panel(title, style="bold blue"))

    def _display_profile_info(self, analysis: ProfileAnalysis):
        table = Table(title="Profile Information", show_header=False)
        table.add_column("Field", style="cyan")
        table.add_column("Value")

        table.add_row("Name", analysis.profile.name or "Not specified")
        table.add_row("Bio", analysis.profile.bio or "Not specified")
        table.add_row("Location", analysis.profile.location or "Not specified")
        table.add_row("Company", analysis.profile.company or "Not specified")
        table.add_row("Public Repos", str(analysis.profile.public_repos))
        table.add_row("Followers", str(analysis.profile.followers))
        table.add_row("Following", str(analysis.profile.following))

        self.console.print(table)

    def _display_repo_stats(self, analysis: ProfileAnalysis):
        table = Table(title="Repository Statistics", show_header=False)
        table.add_column("Metric", style="cyan")
        table.add_column("Value")

        table.add_row("Total Repos", str(len(analysis.repos)))
        table.add_row("Total Stars", str(analysis.total_stars))
        table.add_row("Total Forks", str(analysis.total_forks))

        if analysis.languages:
            lang_parts = [
                f"{lang} ({count})" for lang, count in analysis.languages.items()
            ]
            langs = ", ".join(lang_parts)
            table.add_row("Languages", langs)

        self.console.print(table)

    def _display_languages(self, analysis: ProfileAnalysis):
        table = Table(title="Language Distribution")
        table.add_column("Language", style="cyan")
        table.add_column("Repos", justify="right")
        table.add_column("Distribution", min_width=30)

        total = sum(analysis.languages.values())
        for lang, count in analysis.languages.items():
            percentage = (count / total) * 100
            bar_length = int(percentage / 2)
            bar = "█" * bar_length
            table.add_row(lang, str(count), f"{bar} {percentage:.1f}%")

        self.console.print(table)

    def _display_scores(self, analysis: ProfileAnalysis):
        table = Table(title="Scores", show_header=False)
        table.add_column("Score", style="cyan")
        table.add_column("Value")

        if analysis.activity_score >= 70:
            activity_color = "green"
        elif analysis.activity_score >= 40:
            activity_color = "yellow"
        else:
            activity_color = "red"

        if analysis.completeness_score >= 70:
            completeness_color = "green"
        elif analysis.completeness_score >= 40:
            completeness_color = "yellow"
        else:
            completeness_color = "red"

        activity_str = (
            f"[{activity_color}]{analysis.activity_score}/100[/{activity_color}]"
        )
        completeness_str = (
            f"[{completeness_color}]{analysis.completeness_score}/100"
            f"[/{completeness_color}]"
        )
        table.add_row("Activity Score", activity_str)
        table.add_row("Profile Completeness", completeness_str)

        self.console.print(table)

    def _display_recommendations(self, analysis: ProfileAnalysis):
        table = Table(title="Recommendations", show_header=False)
        table.add_column("No.", style="cyan")
        table.add_column("Recommendation")

        for i, rec in enumerate(analysis.recommendations, 1):
            table.add_row(str(i), rec)

        self.console.print(table)

    def display_error(self, message: str):
        self.console.print(f"[bold red]Error:[/bold red] {message}")
