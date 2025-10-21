# Example Prioritization Feature

## Overview

The github-reader skill **automatically prioritizes examples, demos, and code snippets** when analyzing repositories. This is the most effective way to understand how to use code, as examples show working implementations rather than just API definitions.

## How It Works

### 1. Automatic Detection

When fetching a repository, the skill automatically:
- Scans the repository tree for example directories
- Identifies files in: `examples/`, `demos/`, `samples/`, `tutorials/`, `quickstart/`, `getting-started/`, `snippets/`, `cookbook/`, `recipes/`, `docs/examples/`
- Tracks total count of example files
- Reports availability in response

### 2. Automatic Prioritization

By default (unless `--no-examples` flag is used):
- **Up to half** of `max_files` limit is reserved for examples
- Example files are fetched **before** other files
- Minimum 3 example files are attempted if available
- Examples appear in `file_contents` alongside README and config files

### 3. Response Structure

Every response includes:

```json
{
  "summary": {
    "has_examples": true,        // Boolean - repo has example directories
    "example_count": 19          // Total example files found
  },
  "available_examples": [        // First 20 example file paths
    "examples/basic.py",
    "examples/advanced.py",
    "demos/quickstart.js"
  ],
  "file_contents": {             // Actual file contents (examples prioritized)
    "README.md": "...",
    "examples/basic.py": "..."   // Example files included automatically
  }
}
```

## Why Prioritize Examples?

### Better Learning
- **Working code** - Examples compile/run, showing complete usage
- **Best practices** - Demonstrate recommended patterns
- **Error handling** - Include setup, teardown, edge cases
- **Context** - Show features in realistic scenarios

### More Efficient
- **Concise** - Examples are shorter than main source code
- **Focused** - Demonstrate specific features clearly
- **Self-contained** - Often work standalone without deep dependencies

### Practical Value
- **Copy-paste ready** - Users can adapt examples directly
- **Quick start** - Faster than reading API documentation
- **Pattern matching** - Easy to see how similar to user's needs

## Example Directories Detected

The skill recognizes these directory patterns (case-insensitive):

### Standard Patterns
- `examples/` or `example/`
- `demos/` or `demo/`
- `samples/` or `sample/`

### Tutorial Patterns
- `tutorials/` or `tutorial/`
- `quickstart/`
- `getting-started/`

### Snippet Patterns
- `snippets/`
- `cookbook/`
- `recipes/`

### Documentation Patterns
- `docs/examples/`

## Usage

### Automatic (Default)
```bash
# Examples are automatically prioritized
scripts/fetch_repo.py https://github.com/owner/repo

# Output includes examples in file_contents
```

### Disable Example Prioritization
```bash
# Skip example prioritization
scripts/fetch_repo.py https://github.com/owner/repo --no-examples
```

### Manually Fetch Specific Examples
```bash
# After seeing available_examples in initial response
scripts/fetch_repo.py https://github.com/owner/repo \
  --files examples/advanced.py examples/streaming.py
```

## Claude Workflow Integration

When Claude uses this skill:

1. **Initial fetch** - Automatically includes examples
2. **Check `has_examples`** - Claude verifies if examples exist
3. **Review `available_examples`** - Claude sees what's available
4. **Read `file_contents`** - Claude analyzes fetched examples
5. **Present to user** - Claude shows examples in explanations
6. **Fetch more if needed** - Claude can request specific examples

## Real-World Example

### Anthropic Python SDK

```bash
$ python3 scripts/fetch_repo.py https://github.com/anthropics/anthropic-sdk-python --max-files 8
```

**Result:**
- `has_examples`: `true`
- `example_count`: `19`
- Automatically fetched:
  - `examples/batch_results.py`
  - `examples/bedrock.py`
  - Plus README, pyproject.toml, etc.
- Available for follow-up:
  - `examples/messages.py`
  - `examples/messages_stream.py`
  - `examples/tools.py`
  - ... and 14 more

**User benefit:** Immediate access to working code showing how to use the SDK, without manually searching or specifying file paths.

## Configuration

### Default Behavior
- **Enabled by default** - Examples always prioritized
- **Smart allocation** - Up to 50% of max_files for examples
- **Minimum guarantee** - At least 3 examples if available

### Customization
```bash
# Increase file limit to get more examples
scripts/fetch_repo.py https://github.com/owner/repo --max-files 20

# Disable if only interested in architecture
scripts/fetch_repo.py https://github.com/owner/repo --no-examples
```

## Token Efficiency

Despite prioritizing examples, token usage remains efficient:

- **Selective fetching** - Only fetches examples up to limit
- **Progressive disclosure** - Can fetch more examples on demand
- **Smart filtering** - Skips test files, build artifacts
- **Structured output** - JSON format for efficient parsing

## Best Practices for Claude

When presenting repository analysis to users:

1. **Start with examples** if available in file_contents
2. **Reference example files** by path when explaining concepts
3. **Suggest next steps** using available_examples list
4. **Fetch additional examples** if user needs more detail
5. **Combine examples with docs** for complete understanding

## Future Enhancements

Potential improvements:
- Language-specific example detection (test vs demo files)
- Example quality scoring (file size, comments, imports)
- Category-based filtering (basic, advanced, specific features)
- Example-to-documentation linking
