# Changelog

All notable changes to the GitHub Reader Plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-21

### Added
- Initial release of GitHub Reader Plugin
- API-first repository content fetcher (`fetch_repo.py`)
- Code pattern search tool (`search_code.py`)
- Context-aware filtering for project-relevant examples
- Automatic example and demo prioritization
- Progressive disclosure for token efficiency
- Support for Python 3.8+
- Zero disk usage architecture
- MIT License

### Features
- Fetch repository structure and file contents via GitHub API
- Search code patterns with regex support
- Auto-detect current project languages
- Prioritize examples/demos over source code
- Smart file filtering (skip dependencies, build artifacts)
- Configurable file limits (default 10 files per query)
- Structured JSON output for efficient parsing
- Support for custom branches
- No authentication required for public repositories

### Documentation
- Comprehensive README with usage examples
- Detailed SKILL.md with workflow instructions
- API patterns reference documentation
- Example prioritization guide
- Plugin manifest with metadata

### Limitations
- Public repositories only (no private repo support)
- 60 API requests per hour (unauthenticated)
- Text files only (no binary support)
- Latest commit only (no historical analysis)

[1.0.0]: https://github.com/geniusboywonder/claude-plugins-skills/releases/tag/github-reader-v1.0.0
