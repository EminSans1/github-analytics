"""Tests for GitHub visualizer."""

from io import StringIO

import pytest
from rich.console import Console

from github_analytics.analyzer import ProfileAnalysis, UserProfile, RepoInfo
from github_analytics.visualizer import Visualizer


@pytest.fixture
def visualizer():
    return Visualizer()


@pytest.fixture
def sample_analysis():
    profile = UserProfile(
        username="testuser",
        name="Test User",
        bio="Test bio",
        location="Test location",
        company="Test company",
        blog="https://test.com",
        email="test@test.com",
        public_repos=2,
        followers=10,
        following=5,
        created_at="2020-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        avatar_url="https://example.com/avatar.png",
    )

    repos = [
        RepoInfo(
            name="repo1",
            description="Test repo 1",
            language="Python",
            stars=10,
            forks=5,
            open_issues=2,
            created_at="2020-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
            pushed_at="2024-01-01T00:00:00Z",
            topics=["test"],
        )
    ]

    return ProfileAnalysis(
        profile=profile,
        repos=repos,
        languages={"Python": 1},
        total_stars=10,
        total_forks=5,
        activity_score=75,
        completeness_score=80,
        recommendations=["Add more repositories"],
    )


def test_display_profile(visualizer, sample_analysis):
    console = Console(file=StringIO(), force_terminal=True)
    visualizer.console = console

    visualizer.display_profile(sample_analysis)

    output = console.file.getvalue()
    assert "testuser" in output
    assert "Test User" in output
    assert "Python" in output


def test_display_error(visualizer):
    console = Console(file=StringIO(), force_terminal=True)
    visualizer.console = console

    visualizer.display_error("Test error message")

    output = console.file.getvalue()
    assert "Test error message" in output
    assert "Error" in output