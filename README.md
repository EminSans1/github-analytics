# GitHub Analytics CLI

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#testing)

CLI tool for analyzing GitHub profiles and repositories — activity metrics, language breakdown, quality scoring, and actionable recommendations.

## Features

- **Profile Analysis** — comprehensive overview of any GitHub user's profile
- **Repository Statistics** — breakdown by language, stars, forks, and creation date
- **Activity Metrics** — commit frequency, contribution patterns, and activity trends
- **Language Analysis** — visual bar chart of programming languages used
- **Quality Score** — automated assessment of profile completeness and activity level
- **Recommendations** — actionable suggestions to improve your GitHub presence
- **Markdown Export** — generate formatted reports saved to file

## Installation

```bash
git clone https://github.com/EminSans1/github-analytics.git
cd github-analytics
pip install -e ".[dev]"
```

## Usage

### Profile Analysis

```bash
# Analyze a GitHub user
github-analytics user EminSans1

# Show detailed output
github-analytics user EminSans1 --detailed

# Export report to Markdown
github-analytics user EminSans1 --export report.md
```

### Repository Analysis

```bash
github-analytics repo owner/repo-name
```

### Examples

**Profile Summary:**

```
$ github-analytics user EminSans1

GitHub Profile Analysis: EminSans1
===================================

Profile Information:
  Name: EminSans1
  Bio: Developer
  Public Repos: 6
  Followers: 0

Repository Statistics:
  Total Repos: 6
  Total Stars: 0
  Languages: Python (5), JavaScript (1)

Activity Score: 75/100
Profile Completeness: 40/100
```

**Language Distribution:**

```
Language Distribution:
  Python      ████████████████████ 83.3%
  JavaScript  ████ 16.7%
```

## API Rate Limits

This tool uses the GitHub REST API which has rate limits:
- **Unauthenticated**: 60 requests/hour
- **Authenticated**: 5,000 requests/hour

Set a token for better performance:

```bash
export GITHUB_TOKEN=your_token_here
github-analytics user EminSans1
```

## Development

### Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Tests

```bash
pytest
pytest --cov=github_analytics --cov-report=html
```

### Code Quality

```bash
black github_analytics tests        # Format
ruff check github_analytics tests   # Lint
mypy github_analytics               # Type check
```

## Project Structure

```
github-analytics/
├── github_analytics/
│   ├── __init__.py
│   ├── __main__.py       # Entry point
│   ├── analyzer.py       # Core analysis logic
│   ├── github_api.py     # GitHub API client
│   ├── visualizer.py     # Terminal visualization
│   ├── reporter.py       # Markdown report generation
│   └── cli.py            # CLI interface
├── tests/
│   ├── test_analyzer.py
│   ├── test_github_api.py
│   └── test_visualizer.py
├── pyproject.toml
├── LICENSE
├── README.md
└── .gitignore
```

## Contributing

1. Fork the repository
2. Create your branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License — see [LICENSE](LICENSE) for details.

## Acknowledgments

- [GitHub REST API](https://docs.github.com/en/rest) — data source
- [Rich](https://github.com/Textualize/rich) — terminal visualization
- [Requests](https://github.com/psf/requests) — HTTP client
