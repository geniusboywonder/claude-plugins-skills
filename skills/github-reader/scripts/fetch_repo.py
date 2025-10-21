#!/usr/bin/env python3
"""
GitHub Repository Fetcher - API-First Approach

Fetches repository content using GitHub's API without cloning.
Returns structured JSON with file contents for token-efficient analysis.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from typing import Dict, List, Optional, Any
from pathlib import Path
import re


class GitHubRepoFetcher:
    """Fetches GitHub repository content via API without disk operations."""

    RAW_URL_BASE = "https://raw.githubusercontent.com"
    API_URL_BASE = "https://api.github.com"

    # Key files to always fetch for repository understanding
    KEY_FILES = [
        "README.md", "README.rst", "README.txt", "README",
        "package.json", "requirements.txt", "Cargo.toml", "go.mod",
        "pom.xml", "build.gradle", "setup.py", "pyproject.toml",
        ".gitignore", "LICENSE", "Makefile", "Dockerfile"
    ]

    # Priority directories for examples and usage patterns
    PRIORITY_DIRS = {
        "examples", "example", "demos", "demo", "samples", "sample",
        "tutorials", "tutorial", "quickstart", "getting-started",
        "snippets", "cookbook", "recipes", "docs/examples"
    }

    # Directories to skip for efficiency
    SKIP_DIRS = {
        "node_modules", ".git", "vendor", "dist", "build",
        "__pycache__", ".next", "out", "coverage", ".pytest_cache",
        "target", "bin", "obj", ".vscode", ".idea"
    }

    def __init__(self, repo_url: str, branch: str = "main"):
        """Initialize fetcher with repository URL."""
        self.repo_url = repo_url.rstrip('/')
        self.owner, self.repo = self._parse_repo_url(repo_url)
        self.branch = branch

    def _parse_repo_url(self, url: str) -> tuple[str, str]:
        """Extract owner and repo name from GitHub URL."""
        # Handle: https://github.com/owner/repo or github.com/owner/repo
        pattern = r'github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$'
        match = re.search(pattern, url)
        if not match:
            raise ValueError(f"Invalid GitHub URL: {url}")
        return match.group(1), match.group(2)

    def _fetch_url(self, url: str, is_api: bool = False) -> Any:
        """Fetch URL content with error handling."""
        try:
            headers = {'Accept': 'application/json'} if is_api else {}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read()
                return json.loads(content) if is_api else content.decode('utf-8')
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            raise RuntimeError(f"HTTP {e.code}: {e.reason} - {url}")
        except Exception as e:
            raise RuntimeError(f"Failed to fetch {url}: {str(e)}")

    def fetch_tree_structure(self) -> Dict[str, Any]:
        """Fetch repository tree structure via API."""
        # Try main branch first, fall back to master
        for branch in [self.branch, "master", "main"]:
            url = f"{self.API_URL_BASE}/repos/{self.owner}/{self.repo}/git/trees/{branch}?recursive=1"
            tree = self._fetch_url(url, is_api=True)
            if tree:
                self.branch = branch  # Update to working branch
                return tree

        raise RuntimeError(f"Could not fetch tree for {self.owner}/{self.repo}")

    def fetch_file_content(self, file_path: str) -> Optional[str]:
        """Fetch single file content via raw GitHub URL."""
        url = f"{self.RAW_URL_BASE}/{self.owner}/{self.repo}/{self.branch}/{file_path}"
        return self._fetch_url(url)

    def analyze_tree(self, tree: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze tree structure and categorize files."""
        files = tree.get('tree', [])

        analysis = {
            'total_files': 0,
            'total_dirs': 0,
            'languages': {},
            'structure': {},
            'key_files': [],
            'example_files': [],
            'main_dirs': set(),
            'has_examples': False
        }

        for item in files:
            path = item['path']
            item_type = item['type']

            # Skip unwanted directories
            if any(skip_dir in path.split('/') for skip_dir in self.SKIP_DIRS):
                continue

            if item_type == 'tree':
                analysis['total_dirs'] += 1
                # Track top-level directories
                top_dir = path.split('/')[0]
                analysis['main_dirs'].add(top_dir)

                # Check for example directories
                if any(priority_dir in path.lower().split('/') for priority_dir in self.PRIORITY_DIRS):
                    analysis['has_examples'] = True

            elif item_type == 'blob':
                analysis['total_files'] += 1

                # Detect language by extension
                ext = Path(path).suffix
                if ext:
                    analysis['languages'][ext] = analysis['languages'].get(ext, 0) + 1

                # Track key files
                filename = Path(path).name
                if filename in self.KEY_FILES or path in self.KEY_FILES:
                    analysis['key_files'].append(path)

                # Track example files (prioritize these for understanding usage)
                path_parts = path.lower().split('/')
                if any(priority_dir in path_parts for priority_dir in self.PRIORITY_DIRS):
                    analysis['example_files'].append(path)

        analysis['main_dirs'] = sorted(analysis['main_dirs'])
        return analysis

    def filter_examples_by_context(self, example_files: List[str],
                                   context_extensions: Optional[List[str]] = None) -> List[str]:
        """
        Filter example files to match current project context.

        Args:
            example_files: List of all example file paths
            context_extensions: File extensions from current project (e.g., ['.py', '.tsx'])

        Returns:
            Filtered list of example files matching context (or all if no context)
        """
        if not context_extensions:
            return example_files

        # Filter examples matching project extensions
        matching = []
        non_matching = []

        for file_path in example_files:
            ext = Path(file_path).suffix
            if ext in context_extensions:
                matching.append(file_path)
            else:
                non_matching.append(file_path)

        # Return matching first, then non-matching (in case we need to fill quota)
        return matching + non_matching

    def fetch_key_files(self, key_file_paths: List[str], max_files: int = 10) -> Dict[str, str]:
        """Fetch content of key files."""
        contents = {}

        for i, file_path in enumerate(key_file_paths[:max_files]):
            content = self.fetch_file_content(file_path)
            if content:
                contents[file_path] = content

        return contents

    def search_files_by_pattern(self, tree: Dict[str, Any], pattern: str) -> List[str]:
        """Search for files matching a pattern in the tree."""
        files = tree.get('tree', [])
        matching = []

        regex = re.compile(pattern, re.IGNORECASE)

        for item in files:
            if item['type'] == 'blob':
                path = item['path']
                # Skip unwanted directories
                if any(skip_dir in path.split('/') for skip_dir in self.SKIP_DIRS):
                    continue

                if regex.search(path):
                    matching.append(path)

        return matching

    def fetch_repo(self, query: Optional[str] = None, specific_files: Optional[List[str]] = None,
                   max_files: int = 10, prioritize_examples: bool = True,
                   context_extensions: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Main entry point: Fetch repository with intelligent file selection.

        Args:
            query: Optional search query to find relevant files
            specific_files: Optional list of specific file paths to fetch
            max_files: Maximum number of files to fetch
            prioritize_examples: If True, prioritize example/demo files (default: True)
            context_extensions: File extensions from current project for context filtering

        Returns:
            Structured JSON with repo info and file contents
        """
        # Fetch tree structure
        tree = self.fetch_tree_structure()
        analysis = self.analyze_tree(tree)

        # Determine which files to fetch
        files_to_fetch = []

        if specific_files:
            # User specified exact files
            files_to_fetch = specific_files
        else:
            # Auto-detect key files (README, config, etc.)
            files_to_fetch = analysis['key_files']

            # Prioritize example files if available and requested
            if prioritize_examples and analysis['example_files']:
                # Filter examples by context if provided
                example_files = self.filter_examples_by_context(
                    analysis['example_files'],
                    context_extensions
                )

                # Add example files first (up to half the max_files limit)
                example_limit = max(3, max_files // 2)
                files_to_fetch.extend(example_files[:example_limit])

            # If query provided, search for matching files
            if query:
                matching = self.search_files_by_pattern(tree, query)
                files_to_fetch.extend(matching[:max_files - len(files_to_fetch)])

        # Fetch file contents
        file_contents = self.fetch_key_files(files_to_fetch, max_files)

        # Build response
        response = {
            'repo': f"{self.owner}/{self.repo}",
            'url': self.repo_url,
            'branch': self.branch,
            'summary': {
                'total_files': analysis['total_files'],
                'total_dirs': analysis['total_dirs'],
                'languages': analysis['languages'],
                'main_directories': analysis['main_dirs'],
                'has_examples': analysis['has_examples'],
                'example_count': len(analysis['example_files'])
            },
            'fetched_files': list(file_contents.keys()),
            'available_examples': analysis['example_files'][:20],  # Show first 20 example files
            'file_contents': file_contents
        }

        # Add context filtering info if used
        if context_extensions:
            response['context_filter'] = {
                'enabled': True,
                'extensions': context_extensions,
                'matched_examples': sum(1 for f in files_to_fetch if Path(f).suffix in context_extensions)
            }

        return response


def main():
    parser = argparse.ArgumentParser(
        description='Fetch GitHub repository content via API (no cloning)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Fetch key files from a repository
  fetch_repo.py https://github.com/anthropics/anthropic-sdk-python

  # Search for authentication-related files
  fetch_repo.py https://github.com/owner/repo --query "auth"

  # Fetch specific files
  fetch_repo.py https://github.com/owner/repo --files src/main.py src/utils.py

  # Limit number of files fetched
  fetch_repo.py https://github.com/owner/repo --query "config" --max-files 5
        '''
    )

    parser.add_argument('url', help='GitHub repository URL')
    parser.add_argument('--branch', default='main', help='Branch to fetch (default: main)')
    parser.add_argument('--query', '-q', help='Search pattern to find relevant files')
    parser.add_argument('--files', '-f', nargs='+', help='Specific files to fetch')
    parser.add_argument('--max-files', type=int, default=10, help='Maximum files to fetch (default: 10)')
    parser.add_argument('--tree-only', action='store_true', help='Only fetch tree structure, no file contents')
    parser.add_argument('--no-examples', action='store_true', help='Skip prioritizing example files')
    parser.add_argument('--context', help='File extensions to prioritize (e.g., ".py,.tsx") or "auto" to detect from current dir')
    parser.add_argument('--context-dir', default='.', help='Directory to detect context from (default: current directory)')

    args = parser.parse_args()

    try:
        fetcher = GitHubRepoFetcher(args.url, args.branch)

        # Determine context extensions if requested
        context_extensions = None
        if args.context:
            if args.context.lower() == 'auto':
                # Auto-detect from current directory
                try:
                    from detect_context import ProjectContextDetector
                    detector = ProjectContextDetector(args.context_dir)
                    context_extensions = detector.get_relevant_extensions()
                except ImportError:
                    print("Warning: Could not import detect_context, skipping auto-detection", file=sys.stderr)
            else:
                # Parse comma-separated extensions
                context_extensions = [ext.strip() for ext in args.context.split(',')]

        if args.tree_only:
            # Only fetch and analyze tree
            tree = fetcher.fetch_tree_structure()
            analysis = fetcher.analyze_tree(tree)
            result = {
                'repo': f"{fetcher.owner}/{fetcher.repo}",
                'branch': fetcher.branch,
                'summary': analysis
            }
        else:
            # Full fetch with file contents
            result = fetcher.fetch_repo(
                query=args.query,
                specific_files=args.files,
                max_files=args.max_files,
                prioritize_examples=not args.no_examples,
                context_extensions=context_extensions
            )

        # Output JSON
        print(json.dumps(result, indent=2))

    except Exception as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
