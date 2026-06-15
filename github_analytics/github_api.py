"""GitHub API client for fetching user and repository data."""

from __future__ import annotations

import os
from typing import Any, Optional

import requests


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
        return self._request(f"users/{username}")

    def get_user_repos(
        self, username: str, per_page: int = 100
    ) -> list[dict[str, Any]]:
        repos = []
        page = 1
        while True:
            endpoint = f"users/{username}/repos?per_page={per_page}&page={page}"
            data = self._request(endpoint)
            if not data:
                break
            repos.extend(data)
            if len(data) < per_page:
                break
            page += 1
        return repos

    def get_repo_languages(self, owner: str, repo: str) -> dict[str, int]:
        return self._request(f"repos/{owner}/{repo}/languages")

    def get_repo_commits(
        self, owner: str, repo: str, per_page: int = 100
    ) -> list[dict[str, Any]]:
        return self._request(f"repos/{owner}/{repo}/commits?per_page={per_page}")

    def get_user_events(
        self, username: str, per_page: int = 100
    ) -> list[dict[str, Any]]:
        return self._request(f"users/{username}/events?per_page={per_page}")

    def get_rate_limit(self) -> dict[str, Any]:
        return self._request("rate_limit")
