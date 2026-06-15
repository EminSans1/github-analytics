"""Tests for GitHub analyzer."""

import pytest
import responses

from github_analytics.analyzer import GitHubAnalyzer
from github_analytics.github_api import GitHubAPI


@pytest.fixture
def api():
    return GitHubAPI()


@pytest.fixture
def analyzer(api):
    return GitHubAnalyzer(api)


@responses.activate
def test_analyze_user(analyzer):
    responses.add(
        responses.GET,
        "https://api.github.com/users/testuser",
        json={
            "login": "testuser",
            "name": "Test User",
            "bio": "Test bio",
            "location": "Test location",
            "company": "Test company",
            "blog": "https://test.com",
            "email": "test@test.com",
            "public_repos": 2,
            "followers": 10,
            "following": 5,
            "created_at": "2020-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "avatar_url": "https://example.com/avatar.png",
        },
        status=200,
    )

    responses.add(
        responses.GET,
        "https://api.github.com/users/testuser/repos?per_page=100&page=1",
        json=[
            {
                "name": "repo1",
                "description": "Test repo 1",
                "language": "Python",
                "stargazers_count": 10,
                "forks_count": 5,
                "open_issues_count": 2,
                "created_at": "2020-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "pushed_at": "2024-01-01T00:00:00Z",
                "topics": ["test"],
            }
        ],
        status=200,
    )

    analysis = analyzer.analyze_user("testuser")

    assert analysis.profile.username == "testuser"
    assert analysis.profile.name == "Test User"
    assert len(analysis.repos) == 1
    assert analysis.total_stars == 10
    assert analysis.total_forks == 5
    assert 0 <= analysis.activity_score <= 100
    assert 0 <= analysis.completeness_score <= 100


@responses.activate
def test_analyze_user_detailed(analyzer):
    responses.add(
        responses.GET,
        "https://api.github.com/users/testuser",
        json={
            "login": "testuser",
            "name": "Test User",
            "bio": "Test bio",
            "location": "Test location",
            "company": "Test company",
            "blog": "https://test.com",
            "email": "test@test.com",
            "public_repos": 2,
            "followers": 10,
            "following": 5,
            "created_at": "2020-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "avatar_url": "https://example.com/avatar.png",
        },
        status=200,
    )

    responses.add(
        responses.GET,
        "https://api.github.com/users/testuser/repos?per_page=100&page=1",
        json=[
            {
                "name": "repo1",
                "description": "Test repo 1",
                "language": "Python",
                "stargazers_count": 10,
                "forks_count": 5,
                "open_issues_count": 2,
                "created_at": "2020-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "pushed_at": "2024-01-01T00:00:00Z",
                "topics": ["test"],
            }
        ],
        status=200,
    )

    analysis = analyzer.analyze_user("testuser", detailed=True)

    assert "Python" in analysis.languages
    assert analysis.languages["Python"] == 1
