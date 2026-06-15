"""Tests for GitHub API client."""

import pytest
import responses

from github_analytics.github_api import GitHubAPI


@responses.activate
def test_get_user():
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
            "public_repos": 5,
            "followers": 10,
            "following": 5,
            "created_at": "2020-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "avatar_url": "https://example.com/avatar.png",
        },
        status=200,
    )

    api = GitHubAPI()
    user = api.get_user("testuser")

    assert user["login"] == "testuser"
    assert user["name"] == "Test User"
    assert user["public_repos"] == 5


@responses.activate
def test_get_user_repos():
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

    api = GitHubAPI()
    repos = api.get_user_repos("testuser")

    assert len(repos) == 1
    assert repos[0]["name"] == "repo1"


@responses.activate
def test_get_rate_limit():
    responses.add(
        responses.GET,
        "https://api.github.com/rate_limit",
        json={
            "resources": {
                "core": {"limit": 60, "remaining": 59, "reset": 1234567890}
            }
        },
        status=200,
    )

    api = GitHubAPI()
    rate_limit = api.get_rate_limit()

    assert "resources" in rate_limit
    assert rate_limit["resources"]["core"]["limit"] == 60