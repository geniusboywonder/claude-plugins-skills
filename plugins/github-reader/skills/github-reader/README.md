# GitHub Reader Skill

A Claude Code skill for reading and analyzing public GitHub repositories without cloning them to disk. Uses an API-first approach for maximum token efficiency and zero disk footprint.

## Overview

This skill enables Claude to understand and analyze any public GitHub repository by fetching content via GitHub's public APIs. Instead of cloning entire repositories, it intelligently fetches only the files needed to answer your questions, returning structured JSON with file contents for direct analysis.

## Key Features

### API-First Approach
- **Zero disk usage** - No git cloning required
- **No cleanup needed** - All content fetched via HTTP
- **No authentication** - Works with public repositories (60 API requests/hour limit)
- **Immediate results** - Fetch specific files in seconds

### Token Efficiency
- **Progressive disclosure** - Start with overview, fetch details on demand
- **Context-aware filtering** - Auto-detects your project languages and prioritizes matching examples
- **Example prioritization** - Automatically fetches examples/demos first (best way to learn)
- **Intelligent prioritization** - Auto-fetches key files (README, config files)
- **Configurable limits** - Default max 10 files per query
- **Smart filtering** - Skips unnecessary directories (node_modules, vendor, dist, etc.)
- **Structured output** - JSON format for efficient parsing

### Two Main Tools

#### 1. `fetch_repo.py` - Repository Content Fetcher
Fetches repository structure and file contents, returning structured JSON.

**Capabilities:**
- **Automatically prioritizes examples and demos** - Best way to understand usage
- Auto-detect and fetch key files (README, package.json, requirements.txt, etc.)
- Search for files by name pattern
- Fetch specific file paths
- Get tree structure only (no file contents)
- Supports custom branches
- Configurable file limits

**Usage Examples:**
```bash
# Quick repository overview (auto-fetches key files)
scripts/fetch_repo.py https://github.com/anthropics/anthropic-sdk-python

# Search for authentication-related files
scripts/fetch_repo.py https://github.com/owner/repo --query "auth"

# Fetch specific files
scripts/fetch_repo.py https://github.com/owner/repo --files src/main.py src/config.py

# Get only tree structure (no file contents)
scripts/fetch_repo.py https://github.com/owner/repo --tree-only

# Specify branch
scripts/fetch_repo.py https://github.com/owner/repo --branch develop

# Limit number of files fetched
scripts/fetch_repo.py https://github.com/owner/repo --query "test" --max-files 5

# Context-aware: Auto-detect current project languages (RECOMMENDED)
scripts/fetch_repo.py https://github.com/owner/repo --context auto

# Context-aware: Manually specify extensions
scripts/fetch_repo.py https://github.com/owner/repo --context ".py,.tsx"
```

**Context-Aware Filtering (NEW):**
When you use `--context auto`, the skill automatically:
1. Detects languages in your current project (Python, React, TypeScript, etc.)
2. Prioritizes examples matching your stack
3. Returns Python examples if you're building a Python app, React examples if you're building a React app, etc.

**Example:** Working on a Python + React project and fetching Anthropic's SDK → automatically gets Python examples, not shell scripts or configs

**Output Format:**
```json
{
  "repo": "owner/repo",
  "url": "https://github.com/owner/repo",
  "branch": "main",
  "summary": {
    "total_files": 150,
    "total_dirs": 25,
    "languages": {".py": 45, ".js": 30, ".md": 5},
    "main_directories": ["src", "tests", "docs"],
    "has_examples": true,
    "example_count": 12
  },
  "fetched_files": ["README.md", "package.json", "examples/basic.py"],
  "available_examples": [
    "examples/basic.py",
    "examples/advanced.py",
    "demos/quickstart.js"
  ],
  "file_contents": {
    "README.md": "# Project Name\n...",
    "package.json": "{\n  \"name\": \"...\"\n}",
    "examples/basic.py": "# Basic usage example\n..."
  }
}
```

**Key output fields:**
- `has_examples` - Boolean indicating if repository has example/demo directories
- `example_count` - Total number of example files found
- `available_examples` - List of example file paths (up to 20) ready to fetch
- `file_contents` - Actual file contents, with examples prioritized automatically

#### 2. `search_code.py` - Code Pattern Search
Search for specific code patterns across repository files with context.

**Capabilities:**
- Regex pattern matching
- File type filtering
- Configurable context lines
- Match statistics
- Efficient file searching (default max 20 files)

**Usage Examples:**
```bash
# Search for authentication functions
scripts/search_code.py https://github.com/owner/repo "def authenticate|async def authenticate"

# Search only in Python files
scripts/search_code.py https://github.com/owner/repo "import requests" --files ".*\.py$"

# Search with more context lines
scripts/search_code.py https://github.com/owner/repo "class.*Config" --context 5

# Limit files searched
scripts/search_code.py https://github.com/owner/repo "useState" --max-files 30
```

**Output Format:**
```json
{
  "repo": "owner/repo",
  "branch": "main",
  "pattern": "def authenticate",
  "statistics": {
    "files_searched": 20,
    "files_with_matches": 3,
    "total_matches": 5
  },
  "matches": [
    {
      "file": "src/auth/service.py",
      "line": 42,
      "match": "def authenticate(username, password):",
      "context_before": ["", "class AuthService:", "    \"\"\"Handle user authentication\"\"\""],
      "context_after": ["    # Validate credentials", "    if not username or not password:"]
    }
  ]
}
```

## Technical Approach

### Why API-First?

Traditional approaches to repository analysis involve cloning repositories locally, which has several drawbacks:
- **Disk space** - Repos can be 100MB-500MB+ with full history
- **Time** - Cloning large repos takes minutes
- **Cleanup** - Requires manual deletion or automated cleanup scripts
- **Context window** - Loading entire repos consumes massive tokens

### Our Solution

This skill uses GitHub's public APIs to fetch only what's needed:

1. **Tree Structure API** - Single request returns entire file/directory structure (~10-50KB JSON)
2. **Raw Content URLs** - Direct file access via `raw.githubusercontent.com` (no rate limits)
3. **Intelligent Selection** - Analyze tree to identify key files before fetching
4. **Structured Output** - Return JSON with file contents for Claude to analyze directly

### API Endpoints Used

**Repository Tree (60 requests/hour limit):**
```
GET https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1
```

**Raw File Content (no rate limit):**
```
GET https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}
```

### File Prioritization Strategy

**PRIORITY 1: Examples and Demos (automatically prioritized):**
- `examples/`, `demos/`, `samples/` - Working code examples
- `tutorials/`, `quickstart/`, `getting-started/` - Tutorial code
- `snippets/`, `cookbook/`, `recipes/` - Code snippets
- `docs/examples/` - Documentation examples

**Why prioritize examples:**
- Show actual working code, not just API definitions
- Demonstrate best practices and common patterns
- Include setup, usage, and error handling
- Often more concise and understandable than main source
- Best way to learn how to use a library or framework

**PRIORITY 2: Foundation files:**
- `README.md` / `README.rst` - Project overview
- `package.json` - Node.js dependencies
- `requirements.txt` / `pyproject.toml` - Python dependencies
- `go.mod` / `Cargo.toml` - Go/Rust dependencies
- `Dockerfile` / `Makefile` - Build/deployment

**Fetch based on query:**
- Authentication → `*auth*.py`, `*session*.js`, `middleware/auth*`
- Database → `*model*.py`, `schema.sql`, `migrations/*`
- API → `*route*.js`, `api/*.py`, `*controller*.rb`
- Tests → `test_*.py`, `*.test.js`, `*_spec.rb`

**Skip for efficiency:**
- `node_modules/`, `vendor/`, `dist/`, `build/` - Dependencies/artifacts
- `.git/`, `.github/` - Version control
- `coverage/`, `__pycache__/` - Generated files
- Binary files (images, fonts, compiled binaries)

## How Claude Uses This Skill

When you ask Claude to analyze a GitHub repository, the workflow is:

### 1. Initial Fetch
```bash
scripts/fetch_repo.py https://github.com/owner/repo
```
- Fetches repository tree structure
- Auto-fetches key files (README, config files)
- Returns summary with languages, directories, file counts

### 2. Analyze Content
Claude examines the returned JSON:
- Reviews `summary` for structure and languages
- Reads `file_contents` to understand purpose
- Notes `main_directories` for organization

### 3. Targeted Deep Dive (if needed)
```bash
# Option A: Fetch additional files by query
scripts/fetch_repo.py https://github.com/owner/repo --query "authentication"

# Option B: Search for specific code patterns
scripts/search_code.py https://github.com/owner/repo "authenticate" --files ".*\.py$"
```

### 4. Provide Answer
Claude references actual code from the JSON response, providing:
- File paths and line numbers
- Code snippets with context
- Implementation explanations
- Suggestions for your own code

## Activation Triggers

This skill automatically activates when you:
- Provide a GitHub repository URL
- Ask "how does X implement Y"
- Request "find examples of Z"
- Say "check this GitHub repo"
- Ask "what does this repository do"

## Limitations

- **Public repositories only** - Private repos require authentication (not currently supported)
- **Rate limits** - 60 tree structure API requests per hour (unauthenticated)
- **Large files** - Files >1MB may be slow to fetch
- **Binary files** - Script returns text content only
- **Latest commit only** - No historical analysis (use `git clone` for full history)

## Example Workflows

### Understanding a New Library

**Question:** "How does the Anthropic Python SDK handle authentication?"

**Workflow:**
1. Fetch repository overview
2. Search for authentication patterns in client files
3. Return code snippets showing API key handling
4. Explain pattern and suggest implementation

### Finding Implementation Examples

**Question:** "Find examples of React hooks usage"

**Workflow:**
1. Fetch files matching "hook" pattern
2. Extract relevant code snippets
3. Present examples with explanations
4. Reference file locations for further reading

### Analyzing Project Structure

**Question:** "What's the architecture of this FastAPI project?"

**Workflow:**
1. Fetch tree structure only (`--tree-only`)
2. Analyze directory organization
3. Fetch key files (main.py, routers, models)
4. Explain architecture and patterns

## Installation

This skill is packaged as `github-reader.zip` and can be installed in Claude Code's skills directory:

```bash
# Extract to Claude Code skills directory
unzip github-reader.zip -d ~/.claude/skills/
```

## Reference Documentation

For detailed API patterns, language-specific strategies, and advanced usage:
- See `references/github_api_patterns.md` in the skill directory
- Includes file prioritization rules for Python, JavaScript, Go, Rust, and more
- Provides error handling strategies and optimization techniques

## Requirements

- Python 3.8+
- No external dependencies (uses only Python standard library)
- Internet connection for GitHub API access

## License

This skill is part of the Claude Code skill ecosystem.
