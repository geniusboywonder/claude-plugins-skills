#!/usr/bin/env python3
"""
GitHub Code Search - Find specific patterns in repository files

Searches for code patterns across repository files using GitHub's raw API.
Returns matching snippets with context for analysis.
"""

import argparse
import json
import sys
import re
from typing import List, Dict, Any
from fetch_repo import GitHubRepoFetcher


class GitHubCodeSearcher:
    """Search for code patterns in GitHub repositories."""

    def __init__(self, fetcher: GitHubRepoFetcher):
        self.fetcher = fetcher

    def search_in_file(self, file_path: str, pattern: str, context_lines: int = 3) -> List[Dict[str, Any]]:
        """
        Search for pattern in a single file and return matches with context.

        Args:
            file_path: Path to file in repository
            pattern: Regex pattern to search for
            context_lines: Number of lines before/after match to include

        Returns:
            List of matches with line numbers and context
        """
        content = self.fetcher.fetch_file_content(file_path)
        if not content:
            return []

        lines = content.split('\n')
        matches = []
        regex = re.compile(pattern, re.IGNORECASE)

        for line_num, line in enumerate(lines, start=1):
            if regex.search(line):
                # Extract context
                start_line = max(0, line_num - context_lines - 1)
                end_line = min(len(lines), line_num + context_lines)

                context = {
                    'file': file_path,
                    'line': line_num,
                    'match': line.strip(),
                    'context_before': lines[start_line:line_num-1],
                    'context_after': lines[line_num:end_line]
                }
                matches.append(context)

        return matches

    def search_repository(self, pattern: str, file_pattern: str = None,
                         max_files: int = 20, context_lines: int = 3) -> Dict[str, Any]:
        """
        Search for pattern across repository files.

        Args:
            pattern: Code pattern to search for (regex)
            file_pattern: Optional file path pattern to limit search
            max_files: Maximum number of files to search
            context_lines: Lines of context around matches

        Returns:
            Search results with matches and statistics
        """
        # Fetch repository tree
        tree = self.fetcher.fetch_tree_structure()

        # Find files to search
        if file_pattern:
            files_to_search = self.fetcher.search_files_by_pattern(tree, file_pattern)
        else:
            # Search all code files (skip binary and config)
            code_extensions = {'.py', '.js', '.ts', '.go', '.java', '.rb', '.rs', '.c', '.cpp', '.h', '.php', '.jsx', '.tsx'}
            files = tree.get('tree', [])
            files_to_search = [
                item['path'] for item in files
                if item['type'] == 'blob' and any(item['path'].endswith(ext) for ext in code_extensions)
            ]

        # Limit files to search
        files_to_search = files_to_search[:max_files]

        # Search each file
        all_matches = []
        files_with_matches = set()

        for file_path in files_to_search:
            matches = self.search_in_file(file_path, pattern, context_lines)
            if matches:
                all_matches.extend(matches)
                files_with_matches.add(file_path)

        # Build results
        results = {
            'repo': f"{self.fetcher.owner}/{self.fetcher.repo}",
            'branch': self.fetcher.branch,
            'pattern': pattern,
            'statistics': {
                'files_searched': len(files_to_search),
                'files_with_matches': len(files_with_matches),
                'total_matches': len(all_matches)
            },
            'matches': all_matches[:100]  # Limit to first 100 matches for token efficiency
        }

        return results


def main():
    parser = argparse.ArgumentParser(
        description='Search for code patterns in GitHub repositories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Search for authentication functions
  search_code.py https://github.com/owner/repo "def authenticate|async def authenticate"

  # Search only in Python files
  search_code.py https://github.com/owner/repo "import requests" --files ".*\.py$"

  # Search with custom context
  search_code.py https://github.com/owner/repo "class.*Config" --context 5
        '''
    )

    parser.add_argument('url', help='GitHub repository URL')
    parser.add_argument('pattern', help='Code pattern to search (regex)')
    parser.add_argument('--branch', default='main', help='Branch to search (default: main)')
    parser.add_argument('--files', help='File pattern to limit search (regex)')
    parser.add_argument('--max-files', type=int, default=20, help='Maximum files to search (default: 20)')
    parser.add_argument('--context', type=int, default=3, help='Context lines around matches (default: 3)')

    args = parser.parse_args()

    try:
        fetcher = GitHubRepoFetcher(args.url, args.branch)
        searcher = GitHubCodeSearcher(fetcher)

        results = searcher.search_repository(
            pattern=args.pattern,
            file_pattern=args.files,
            max_files=args.max_files,
            context_lines=args.context
        )

        print(json.dumps(results, indent=2))

    except Exception as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
