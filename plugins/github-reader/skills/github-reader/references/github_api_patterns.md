# GitHub API Access Patterns

This reference document provides patterns for accessing GitHub repository data via API without authentication.

## API Endpoints (No Auth Required for Public Repos)

### Repository Tree Structure
```
GET https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1
```
Returns complete file tree in single request. Typical response: 10-50KB JSON.

**Rate Limit:** 60 requests/hour (unauthenticated)

### Raw File Content
```
GET https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}
```
Returns file content directly. No rate limit for raw content.

### Repository Metadata
```
GET https://api.github.com/repos/{owner}/{repo}
```
Returns repo info: stars, forks, description, default branch, languages, etc.

## Common Repository Analysis Patterns

### Pattern 1: Quick Repository Overview
**Goal:** Understand repository structure and key files without downloading anything.

**Steps:**
1. Fetch tree structure (1 API call)
2. Analyze tree to identify key files and directories
3. Fetch README and main config files (2-5 raw requests)
4. Return structured summary

**Token Cost:** Minimal (~2-5K tokens)

### Pattern 2: Find Specific Implementation
**Goal:** Locate and understand how a specific feature is implemented.

**Steps:**
1. Fetch tree structure
2. Search tree for relevant file paths (e.g., files containing "auth")
3. Fetch identified files
4. Search file contents for specific patterns
5. Return matching code snippets with context

**Token Cost:** Low (~5-10K tokens)

### Pattern 3: Extract Code Examples
**Goal:** Find example usage patterns for implementing similar functionality.

**Steps:**
1. Identify example/demo directories from tree
2. Fetch example files
3. Extract relevant code blocks
4. Return annotated examples

**Token Cost:** Medium (~10-20K tokens depending on examples)

## File Prioritization Strategy

### PRIORITY 1: Examples and Demos (ALWAYS CHECK FIRST)
**Why prioritize examples:**
- Examples show actual working code, not just API definitions
- Demonstrate best practices and common patterns
- Include setup, usage, and error handling
- Often more concise and understandable than main source

**Priority directories to check:**
- `examples/`, `example/` - Standard example directories
- `demos/`, `demo/` - Demo applications
- `samples/`, `sample/` - Code samples
- `tutorials/`, `tutorial/` - Tutorial code
- `quickstart/`, `getting-started/` - Quick start guides
- `snippets/` - Code snippets
- `cookbook/`, `recipes/` - Recipe-style examples
- `docs/examples/` - Documentation examples

**When to prioritize examples:**
- User asks "how do I use X"
- User wants to understand implementation patterns
- User asks for code examples or demonstrations
- Learning about a new library or framework

### PRIORITY 2: Foundation Files
- `README.md` / `README.rst` - Project overview
- `package.json` - Node.js dependencies and scripts
- `requirements.txt` / `pyproject.toml` - Python dependencies
- `go.mod` / `Cargo.toml` - Go/Rust dependencies
- `Dockerfile` / `docker-compose.yml` - Deployment config
- `Makefile` - Build commands
- `.gitignore` - Indicates important file types

### PRIORITY 3: Fetch Based on Query
**For authentication implementation:**
- Search for: `auth`, `login`, `session`, `jwt`, `oauth`
- File patterns: `*auth*.py`, `*session*.js`, `middleware/auth*`

**For database schema:**
- Search for: `models`, `schema`, `migrations`, `database`
- File patterns: `*model*.py`, `schema.sql`, `migrations/*`

**For API endpoints:**
- Search for: `routes`, `api`, `handlers`, `controllers`
- File patterns: `*route*.js`, `api/*.py`, `*controller*.rb`

**For testing patterns:**
- Search for: `test`, `spec`, `__tests__`
- File patterns: `test_*.py`, `*.test.js`, `*_spec.rb`

### Skip for Efficiency
- `node_modules/`, `vendor/`, `dist/`, `build/` - Dependencies/build artifacts
- `.git/`, `.github/workflows/` - Version control internals
- `coverage/`, `.pytest_cache/`, `__pycache__/` - Test/cache artifacts
- Binary files: images, fonts, compiled binaries

## Language-Specific Entry Points

### Python Projects
**Priority files:**
1. `README.md`
2. `pyproject.toml` / `setup.py` / `requirements.txt`
3. `src/__init__.py` or `{package}/__init__.py`
4. `main.py` / `app.py` / `manage.py`

**Common patterns:**
- Package structure: `src/{package}/` or `{package}/`
- Tests: `tests/` or `{package}/tests/`
- Config: `config/` or `settings.py`

### JavaScript/TypeScript Projects
**Priority files:**
1. `README.md`
2. `package.json`
3. `src/index.ts` or `index.js`
4. `tsconfig.json` / `babel.config.js`

**Common patterns:**
- Source: `src/` or `lib/`
- Tests: `__tests__/` or `*.test.js`
- Config: `config/` or root config files

### Go Projects
**Priority files:**
1. `README.md`
2. `go.mod`
3. `main.go`
4. `Makefile`

**Common patterns:**
- Package structure: `pkg/`, `cmd/`, `internal/`
- Tests: `*_test.go` files

### Rust Projects
**Priority files:**
1. `README.md`
2. `Cargo.toml`
3. `src/main.rs` or `src/lib.rs`

**Common patterns:**
- Source: `src/`
- Tests: `tests/` or inline in source files

## Response Size Management

### Typical File Sizes
- README: 2-10KB (500-2500 tokens)
- Config files: 0.5-5KB (100-1250 tokens)
- Source files: 1-20KB (250-5000 tokens)
- Large files (>50KB): Consider fetching partially or summarizing

### Token Efficiency Rules
1. **Limit fetched files:** Default max 10 files per query
2. **Truncate large files:** If file >100KB, fetch only relevant sections
3. **Return structured summaries:** Instead of full file dumps, extract key information
4. **Progressive disclosure:** Start with overview, fetch details on demand

## Error Handling

### Common Issues
- **404 on tree fetch:** Branch doesn't exist, try "main" then "master"
- **404 on raw content:** File path incorrect or file doesn't exist at that branch
- **Rate limit (403):** Wait 1 hour or use authenticated requests (future enhancement)
- **Timeout:** Repository too large, use sparse approach or clone fallback

### Graceful Degradation
1. If API fails, suggest manual clone
2. If file too large, return truncated version with warning
3. If pattern finds too many matches, return first N with statistics
