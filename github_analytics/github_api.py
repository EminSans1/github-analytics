"""GitHub API client for fetching user and repository data."""

from __future__ import annotations

import os
import re
from typing import Any, Optional
from urllib.parse import quote

import requests


def _validate_github_name(name: str) -> str:
    """Validate and sanitize a GitHub username or repo name for URL paths."""
    if not re.fullmatch(r'[A-Za-z0-9._-]+', name):
        raise ValueError(f"Invalid GitHub name: {name!r}")
    return quote(name, safe='')


class GitHubAPI:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.session = requests.Session()
        if self.token:
            self.session.headers["Authorization"] = f"token {self.token}"
        self.session.headers["Accept"] = "application/vnd.github.v3+json"
        self.session.headers["User-Agent"] = "GitHub-Analytics-CLI"

    def _request(self, endpoint: str) -> dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_user(self, username: str) -> dict[str, Any]:
        return self._request(f"users/{_validate_github_name(username)}")

    def get_user_repos(
        self, username: str, per_page: int = 100
    ) -> list[dict[str, Any]]:
        repos = []
        page = 1
        safe_username = _validate_github_name(username)
        while True:
            endpoint = f"users/{safe_username}/repos?per_page={per_page}&page={page}"
            data = self._request(endpoint)
            if not data:
                break
            repos.extend(data)
            if len(data) < per_page:
                break
            page += 1
        return repos

    def get_repo_languages(self, owner: str, repo: str) -> dict[str, int]:
        return self._request(f"repos/{_validate_github_name(owner)}/{_validate_github_name(repo)}/languages")

    def get_repo_commits(
        self, owner: str, repo: str, per_page: int = 100
    ) -> list[dict[str, Any]]:
        return self._request(f"repos/{_validate_github_name(owner)}/{_validate_github_name(repo)}/commits?per_page={per_page}")

    def get_user_events(
        self, username: str, per_page: int = 100
    ) -> list[dict[str, Any]]:
        return self._request(f"users/{_validate_github_name(username)}/events?per_page={per_page}")

    def get_rate_limit(self) -> dict[str, Any]:
        return self._request("rate_limit")
