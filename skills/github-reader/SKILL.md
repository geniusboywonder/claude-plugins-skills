---
name: github-reader
description: Read and analyze public GitHub repositories using API-first approach without cloning. Use when user references GitHub URLs, asks to find code examples, understand repository structure, or implement features based on existing GitHub projects. Activates on phrases like "check this GitHub repo", "how does X implement Y", "find examples of", or when GitHub URLs are provided.
---

# GitHub Repository Reader

Read and understand public GitHub repositories without cloning them to disk. Uses GitHub's API and raw content endpoints to fetch repository structure and specific files on-demand, returning content directly for token-efficient analysis.

## When to Use This Skill

Activate this skill when:
- User provides a GitHub repository URL
- User asks to "find examples" or "see how X implements Y"
- User requests understanding of a specific GitHub codebase
- User wants code snippets or implementation patterns from GitHub
- User says "check this repo" or "look at this GitHub project"

## How This Skill Works

### Core Principle: Zero Disk Usage, API-First
This skill fetches repository content via HTTP APIs, returning file contents directly in JSON format. No git cloning, no local filesystem operations, no cleanup required.

### Available Scripts

#### 1. `fetch_repo.py` - Main Repository Fetcher
Fetches repository content and returns structured JSON with file contents.

**Usage:**
```bash
# Fetch key files (README, package.json, etc.)
scripts/fetch_repo.py https://github.com/owner/repo

# Search for specific files
scripts/fetch_repo.py https://github.com/owner/repo --query "authentication"

# Fetch specific files
scripts/fetch_repo.py https://github.com/owner/repo --files src/main.py src/config.py

# Get only tree structure (no file contents)
scripts/fetch_repo.py https://github.com/owner/repo --tree-only

# Specify branch
scripts/fetch_repo.py https://github.com/owner/repo --branch develop

# Limit files fetched
scripts/fetch_repo.py https://github.com/owner/repo --query "test" --max-files 5

# Context-aware filtering (auto-detect current project languages)
scripts/fetch_repo.py https://github.com/owner/repo --context auto

# Context-aware filtering (manual extensions)
scripts/fetch_repo.py https://github.com/owner/repo --context ".py,.tsx"
```

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
    "main_directories": ["src", "tests", "docs"]
  },
  "fetched_files": ["README.md", "package.json", "src/index.js"],
  "file_contents": {
    "README.md": "# Project Name\n...",
    "package.json": "{\n  \"name\": \"...\"\n}",
    "src/index.js": "import { foo } from './foo';\n..."
  }
}
```

#### 2. `search_code.py` - Code Pattern Search
Search for specific code patterns across repository files.

**Usage:**
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

## Workflow Instructions

### Context-Aware Repository Analysis (RECOMMENDED)

When user asks to understand or analyze a GitHub repository, **ALWAYS use context-aware filtering** to match examples to their current project:

1. **Initial Fetch with Auto-Context** - Run `fetch_repo.py` with `--context auto`
   - Automatically detects current project languages (Python, React, TypeScript, etc.)
   - Prioritizes examples matching current project's file extensions
   - Fetches most relevant examples first
   ```bash
   scripts/fetch_repo.py https://github.com/owner/repo --context auto
   ```

2. **Check Context Filter Results** - Examine the response
   - **CHECK `context_filter.enabled`** - Confirms filtering was applied
   - **CHECK `context_filter.extensions`** - Shows detected extensions (.py, .tsx, etc.)
   - **CHECK `context_filter.matched_examples`** - Count of matching examples fetched
   - **Result:** Examples in `file_contents` will match user's current project stack

### Standard Repository Analysis Workflow

When context detection is not needed or unavailable:

1. **Initial Fetch** - Run `fetch_repo.py` with the repository URL
   - Script automatically fetches key files (README, config files)
   - **AUTOMATICALLY PRIORITIZES EXAMPLES** - Fetches example/demo files first
   - Returns repository summary and file contents in JSON

2. **Analyze Returned Content** - Examine the JSON output
   - **CHECK `has_examples`** - If true, repository has example/demo directories
   - **CHECK `available_examples`** - List of example files available to fetch
   - Review `summary` for repository structure and languages
   - Read `file_contents` to understand project purpose and architecture
   - **PRIORITIZE EXAMPLES** in explanations to user

3. **Fetch Examples** (if available and helpful) - Get example/demo code
   - Check if `has_examples` is true in the response
   - Use `--files` to fetch specific examples from `available_examples` list
   - Examples are the BEST way to show users how to use the code

4. **Targeted Deep Dive** (if needed) - Fetch additional specific files
   - Use `--query` flag to find relevant files by name pattern
   - Use `--files` flag to fetch exact file paths discovered in step 2
   - Use `search_code.py` to find specific code patterns

5. **Extract Implementation Details** - Answer user's specific question
   - **START WITH EXAMPLES** if available in `file_contents`
   - Reference actual code from `file_contents` in the JSON response
   - Provide file paths and line context when explaining implementations
   - Suggest similar patterns for user's own implementation

### Example: User Asks "How does Anthropic's SDK handle authentication?"

**Step 1:** Fetch repository overview
```bash
scripts/fetch_repo.py https://github.com/anthropics/anthropic-sdk-python
```

**Step 2:** Analyze returned JSON
- Check `summary.main_directories` to locate source code
- Read README.md from `file_contents` to understand authentication approach

**Step 3:** Search for authentication implementation
```bash
scripts/search_code.py https://github.com/anthropics/anthropic-sdk-python "api_key|auth" --files ".*client.*\.py$"
```

**Step 4:** Provide answer based on returned code snippets
- Reference specific file paths and code from JSON response
- Explain authentication pattern found
- Suggest implementation approach for user's project

### Example: User Asks "Find examples of React hooks usage"

**Step 1:** Fetch repository with query
```bash
scripts/fetch_repo.py https://github.com/facebook/react --query "use.*hook|useState|useEffect" --max-files 8
```

**Step 2:** Analyze returned examples
- Review matched files in `fetched_files`
- Extract relevant code snippets from `file_contents`

**Step 3:** If more examples needed, search for specific patterns
```bash
scripts/search_code.py https://github.com/facebook/react "useState.*=|useEffect\(" --files ".*examples.*\.js$"
```

**Step 4:** Present examples to user
- Show actual code from response
- Explain pattern and usage
- Provide file references for further reading

## Token Efficiency Guidelines

### Minimize Token Usage
1. **Start with tree-only** if user just wants overview: `--tree-only`
2. **Limit files fetched** to only what's necessary: `--max-files 5`
3. **Use targeted queries** instead of fetching entire repositories
4. **Reference, don't dump** - Extract relevant snippets, don't show full file contents to user

### Progressive Disclosure
1. **First request:** Fetch repository summary and key files
2. **Second request (if needed):** Fetch specific files identified in step 1
3. **Third request (if needed):** Search for specific code patterns
4. **Avoid:** Fetching entire repository at once

### File Selection Strategy
**Priority 1: Examples and demos (ALWAYS PRIORITIZE):**
- examples/, example/, demos/, demo/, samples/, sample/
- tutorials/, tutorial/, quickstart/, getting-started/
- snippets/, cookbook/, recipes/, docs/examples/
- **Why:** Best way to understand how to use the code

**Priority 2: Foundation files:**
- README.md - Project overview
- package.json / requirements.txt / go.mod - Dependencies
- Dockerfile / Makefile - Build/deployment info

**Priority 3: Based on user query:**
- Authentication → search for "auth", "login", "session"
- Database → search for "model", "schema", "migration"
- API → search for "route", "endpoint", "handler"
- Tests → search for "test", "spec"

**Skip for efficiency:**
- node_modules/, vendor/, dist/, build/ - Dependencies
- .git/, .github/ - Version control
- Binary files, images, fonts

Reference `references/github_api_patterns.md` for detailed patterns and language-specific strategies.

## Error Handling

### Common Issues and Solutions

**Branch not found (404):**
- Default branch may be "master" instead of "main"
- Script automatically tries both, but specify with `--branch` if needed

**Rate limit exceeded (403):**
- GitHub API allows 60 requests/hour without authentication
- Wait 1 hour or space out requests
- Raw content (actual file fetching) has no rate limit

**Repository too large:**
- Use `--tree-only` first to analyze structure
- Fetch only specific directories with `--query`
- Use `--max-files` to limit downloads

**File not found:**
- Verify file path exists in tree structure
- Check branch name is correct
- File may have been renamed/moved in latest commit

## Important Notes

### No Authentication Required
Public repositories require no GitHub API tokens or authentication. Rate limit is 60 API requests per hour for tree structure queries. Raw file content has no rate limit.

### No Disk Cleanup Needed
All content is fetched via HTTP and returned in JSON. No files are written to disk. No cleanup commands necessary.

### Limitations
- **Public repositories only** - Private repos require authentication (not supported)
- **Rate limits** - 60 tree structure requests per hour (unauthenticated)
- **Large files** - Files >1MB may be slow to fetch, consider fetching partially
- **Binary files** - Script returns text content only, skips binaries

### When NOT to Use This Skill
- User wants to clone repository for local development → Suggest `git clone`
- Repository is private → Requires authentication, suggest manual access
- Need complete repository history → API fetches latest commit only
- Working with very large repositories (>10K files) → Consider sparse approach or direct clone

## Reference Documentation

For detailed API patterns, language-specific strategies, and file prioritization rules, reference:
- `references/github_api_patterns.md` - Comprehensive API usage patterns
