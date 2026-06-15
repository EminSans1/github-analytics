"""Core analysis logic for GitHub profiles and repositories."""

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from .github_api import GitHubAPI


@dataclass
class UserProfile:
    username: str
    name: Optional[str]
    bio: Optional[str]
    location: Optional[str]
    company: Optional[str]
    blog: Optional[str]
    email: Optional[str]
    public_repos: int
    followers: int
    following: int
    created_at: str
    updated_at: str
    avatar_url: str


@dataclass
class RepoInfo:
    name: str
    description: Optional[str]
    language: Optional[str]
    stars: int
    forks: int
    open_issues: int
    created_at: str
    updated_at: str
    pushed_at: str
    topics: list[str] = field(default_factory=list)


@dataclass
class ProfileAnalysis:
    profile: UserProfile
    repos: list[RepoInfo]
    languages: dict[str, int]
    total_stars: int
    total_forks: int
    activity_score: int
    completeness_score: int
    recommendations: list[str]


class GitHubAnalyzer:
    def __init__(self, api: GitHubAPI):
        self.api = api

    def analyze_user(self, username: str, detailed: bool = False) -> ProfileAnalysis:
        user_data = self.api.get_user(username)
        profile = self._parse_profile(user_data)

        repos_data = self.api.get_user_repos(username)
        repos = [self._parse_repo(repo) for repo in repos_data]

        languages = self._aggregate_languages(repos_data) if detailed else {}
        total_stars = sum(repo.stars for repo in repos)
        total_forks = sum(repo.forks for repo in repos)

        activity_score = self._calculate_activity_score(repos, user_data)
        completeness_score = self._calculate_completeness_score(user_data)
        recommendations = self._generate_recommendations(user_data, repos)

        return ProfileAnalysis(
            profile=profile,
            repos=repos,
            languages=languages,
            total_stars=total_stars,
            total_forks=total_forks,
            activity_score=activity_score,
            completeness_score=completeness_score,
            recommendations=recommendations,
        )

    def _parse_profile(self, data: dict[str, Any]) -> UserProfile:
        return UserProfile(
            username=data["login"],
            name=data.get("name"),
            bio=data.get("bio"),
            location=data.get("location"),
            company=data.get("company"),
            blog=data.get("blog"),
            email=data.get("email"),
            public_repos=data["public_repos"],
            followers=data["followers"],
            following=data["following"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            avatar_url=data["avatar_url"],
        )

    def _parse_repo(self, data: dict[str, Any]) -> RepoInfo:
        return RepoInfo(
            name=data["name"],
            description=data.get("description"),
            language=data.get("language"),
            stars=data["stargazers_count"],
            forks=data["forks_count"],
            open_issues=data["open_issues_count"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            pushed_at=data["pushed_at"],
            topics=data.get("topics", []),
        )

    def _aggregate_languages(self, repos: list[dict[str, Any]]) -> dict[str, int]:
        languages = Counter()
        for repo in repos:
            if repo.get("language"):
                languages[repo["language"]] += 1
        return dict(languages.most_common())

    def _calculate_activity_score(
        self, repos: list[RepoInfo], user_data: dict[str, Any]
    ) -> int:
        score = 0

        if repos:
            score += min(len(repos) * 5, 30)

        total_stars = sum(repo.stars for repo in repos)
        score += min(total_stars * 2, 30)

        has_recent_push = any(
            self._is_recent(repo.pushed_at) for repo in repos
        )
        if has_recent_push:
            score += 20

        if user_data.get("followers", 0) > 0:
            score += 10

        if user_data.get("bio"):
            score += 10

        return min(score, 100)

    def _calculate_completeness_score(self, user_data: dict[str, Any]) -> int:
        score = 0
        profile_fields = ["name", "bio", "location", "company", "blog", "email"]
        for profile_field in profile_fields:
            if user_data.get(profile_field):
                score += 15

        if user_data.get("avatar_url"):
            score += 10

        return min(score, 100)

    def _generate_recommendations(
        self, user_data: dict[str, Any], repos: list[RepoInfo]
    ) -> list[str]:
        recommendations = []

        if not user_data.get("bio"):
            recommendations.append("Add a bio to your profile to introduce yourself")

        if not user_data.get("location"):
            recommendations.append("Add your location to help others connect with you")

        if not user_data.get("company"):
            recommendations.append("Add your company or organization")

        if not user_data.get("blog"):
            recommendations.append("Add a blog or website link")

        if len(repos) < 5:
            recommendations.append("Create more repositories to showcase your skills")

        if not any(repo.stars > 0 for repo in repos):
            recommendations.append("Add interesting content to attract stars")

        return recommendations

    def _is_recent(self, date_str: str) -> bool:
        try:
            date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            now = datetime.now(date.tzinfo)
            return (now - date).days <= 30
        except (ValueError, TypeError):
            return False
