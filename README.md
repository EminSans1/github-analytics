# GitHub Analytics CLI

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#testing)

A powerful CLI tool for analyzing GitHub profiles and repositories. Get insights into your GitHub activity, languages, and contribution patterns.

## Features

- **Profile Analysis**: Comprehensive overview of any GitHub user's profile
- **Repository Statistics**: Detailed breakdown of repositories by language, stars, forks
- **Activity Metrics**: Commit frequency, contribution patterns, and activity trends
- **Language Analysis**: Visual representation of programming languages used
- **Quality Score**: Automated assessment of profile completeness and activity
- **Recommendations**: Actionable suggestions to improve your GitHub presence
- **Markdown Export**: Generate beautiful reports in Markdown format

## Installation

```bash
# Clone the repository
git clone https://github.com/EminSans1/github-analytics.git
cd github-analytics

# Install in development mode
pip install -e ".[dev]"
```

## Usage

### Basic Analysis

```bash
# Analyze a GitHub user
github-analytics user EminSans1

# Analyze with detailed output
github-analytics user EminSans1 --detailed

# Export report to Markdown
github-analytics user EminSans1 --export report.md
```

### Repository Analysis

```bash
# Analyze specific repository
github-analytics repo EminSans1/system-monitor

# Compare repositories
github-analytics compare repo1 repo2
```

### Profile Comparison

```bash
# Compare two GitHub profiles
github-analytics compare user1 user2
```

## Examples

### Profile Summary

```
$ github-analytics user EminSans1

GitHub Profile Analysis: EminSans1
===================================

Profile Information:
  Name: EminSans1
  Bio: Developer
  Location: Not specified
  Company: Not specified
  Public Repos: 6
  Followers: 0
  Following: 0

Repository Statistics:
  Total Repos: 6
  Total Stars: 0
  Total Forks: 0
  Languages: Python (5), JavaScript (1)

Activity Score: 75/100
Profile Completeness: 40/100
```

### Language Distribution

```
Language Distribution:
  Python      ████████████████████ 83.3%
  JavaScript  ████ 16.7%
```

### Recommendations

```
Recommendations:
  1. Add a profile README to showcase your projects
  2. Complete your profile information (bio, location, company)
  3. Add more stars to repositories you find useful
  4. Consider adding more documentation to your projects
```

## Architecture

```
github-analytics/
├── github_analytics/
│   ├── __init__.py
│   ├── analyzer.py      # Core analysis logic
│   ├── github_api.py    # GitHub API client
│   ├── visualizer.py    # Terminal visualization
│   ├── reporter.py      # Report generation
│   └── cli.py           # CLI interface
├── tests/
│   ├── test_analyzer.py
│   ├── test_github_api.py
│   └── test_visualizer.py
├── pyproject.toml
├── README.md
└── LICENSE
```

## API Rate Limits

This tool uses the GitHub REST API which has rate limits:
- **Unauthenticated**: 60 requests per hour
- **Authenticated**: 5,000 requests per hour

For better performance, you can set a GitHub token:

```bash
export GITHUB_TOKEN=your_token_here
github-analytics user EminSans1
```

## Development

### Setup

```bash
# Clone and install
git clone https://github.com/EminSans1/github-analytics.git
cd github-analytics
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=github_analytics --cov-report=html
```

### Code Quality

```bash
# Format code
black github_analytics tests

# Lint code
ruff check github_analytics tests

# Type checking
mypy github_analytics
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [GitHub REST API](https://docs.github.com/en/rest) for providing the data
- [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- [Requests](https://github.com/psf/requests) for HTTP client