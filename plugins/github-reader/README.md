# GitHub Reader Plugin

A Claude Code plugin for reading and analyzing public GitHub repositories without cloning them to disk. Uses an API-first approach for maximum token efficiency and zero disk footprint.

## Installation

### From Marketplace

```bash
# Coming soon - will be available in Claude Code marketplace
```

### Manual Installation

1. Download the latest release
2. Extract to your Claude Code plugins directory:

```bash
# Extract the plugin
unzip github-reader-plugin.zip -d ~/.claude/plugins/

# Or clone from the marketplace repository
git clone https://github.com/geniusboywonder/claude-plugins-skills.git
cp -r claude-plugins-skills/plugins/github-reader ~/.claude/plugins/
```

3. Restart Claude Code or reload plugins

## Features

### API-First Approach
- **Zero disk usage** - No git cloning required
- **No cleanup needed** - All content fetched via HTTP
- **No authentication** - Works with public repositories (60 API requests/hour limit)
- **Immediate results** - Fetch specific files in seconds

### Intelligent Content Discovery
- **Context-aware filtering** - Auto-detects your project languages and prioritizes matching examples
- **Example prioritization** - Automatically fetches examples/demos first (best way to learn)
- **Progressive disclosure** - Start with overview, fetch details on demand
- **Smart filtering** - Skips unnecessary directories (node_modules, vendor, dist, etc.)

### Two Main Tools

#### 1. Repository Content Fetcher (`fetch_repo.py`)
Fetches repository structure and file contents, returning structured JSON.

**Usage:**
```bash
# Quick repository overview (auto-fetches key files)
scripts/fetch_repo.py https://github.com/anthropics/anthropic-sdk-python

# Context-aware: Auto-detect current project languages (RECOMMENDED)
scripts/fetch_repo.py https://github.com/owner/repo --context auto

# Search for specific files
scripts/fetch_repo.py https://github.com/owner/repo --query "auth"

# Fetch specific files
scripts/fetch_repo.py https://github.com/owner/repo --files src/main.py src/config.py
```

#### 2. Code Pattern Search (`search_code.py`)
Search for specific code patterns across repository files with context.

**Usage:**
```bash
# Search for authentication functions
scripts/search_code.py https://github.com/owner/repo "def authenticate"

# Search only in Python files
scripts/search_code.py https://github.com/owner/repo "import requests" --files ".*\.py$"
```

## How It Works

### Context-Aware Filtering

When you use `--context auto`, the plugin automatically:
1. Detects languages in your current project (Python, React, TypeScript, etc.)
2. Prioritizes examples matching your stack
3. Returns Python examples if you're building a Python app, React examples if you're building a React app

**Example:** Working on a Python + React project and fetching Anthropic's SDK → automatically gets Python examples, not shell scripts or configs

### Example Prioritization

The plugin automatically prioritizes:
- `examples/`, `demos/`, `samples/` - Working code examples
- `tutorials/`, `quickstart/`, `getting-started/` - Tutorial code
- `snippets/`, `cookbook/`, `recipes/` - Code snippets
- `docs/examples/` - Documentation examples

Examples are the best way to understand how to use a library or framework.

## Usage Examples

### Understanding a New Library

**Question:** "How does the Anthropic Python SDK handle authentication?"

Claude will:
1. Fetch repository overview
2. Search for authentication patterns in client files
3. Return code snippets showing API key handling
4. Explain pattern and suggest implementation

### Finding Implementation Examples

**Question:** "Find examples of React hooks usage"

Claude will:
1. Fetch files matching "hook" pattern with context filtering
2. Extract relevant code snippets matching your React project
3. Present examples with explanations
4. Reference file locations for further reading

### Analyzing Project Structure

**Question:** "What's the architecture of this FastAPI project?"

Claude will:
1. Fetch tree structure only (`--tree-only`)
2. Analyze directory organization
3. Fetch key files (main.py, routers, models)
4. Explain architecture and patterns

## Activation Triggers

This plugin automatically activates when you:
- Provide a GitHub repository URL
- Ask "how does X implement Y"
- Request "find examples of Z"
- Say "check this GitHub repo"
- Ask "what does this repository do"

## Requirements

- Python 3.8+
- No external dependencies (uses only Python standard library)
- Internet connection for GitHub API access

## Limitations

- **Public repositories only** - Private repos require authentication (not currently supported)
- **Rate limits** - 60 tree structure API requests per hour (unauthenticated)
- **Large files** - Files >1MB may be slow to fetch
- **Binary files** - Returns text content only
- **Latest commit only** - No historical analysis

## Technical Details

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

1. **Examples and Demos** - Automatically prioritized
2. **Foundation files** - README, package.json, requirements.txt
3. **Query-based** - Files matching user's specific request
4. **Skip** - Dependencies, build artifacts, version control

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

- Issues: https://github.com/geniusboywonder/claude-plugins-skills/issues
- Discussions: https://github.com/geniusboywonder/claude-plugins-skills/discussions

## Author

Neill Adamson

## Version

1.0.0
