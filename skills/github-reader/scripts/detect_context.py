#!/usr/bin/env python3
"""
Project Context Detection - Detect languages and frameworks in current project

Analyzes the current working directory to determine:
- Programming languages (Python, JavaScript/TypeScript, Go, Rust, etc.)
- Frameworks (React, Vue, FastAPI, Django, etc.)
- Returns list of relevant file extensions to prioritize
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Set


class ProjectContextDetector:
    """Detect languages and frameworks in current project directory."""

    # Language indicators
    LANGUAGE_INDICATORS = {
        'python': {
            'extensions': ['.py'],
            'files': ['requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile'],
            'dirs': ['venv', '.venv', '__pycache__']
        },
        'javascript': {
            'extensions': ['.js', '.jsx', '.mjs'],
            'files': ['package.json', 'package-lock.json', 'yarn.lock'],
            'dirs': ['node_modules']
        },
        'typescript': {
            'extensions': ['.ts', '.tsx'],
            'files': ['tsconfig.json', 'package.json'],
            'dirs': ['node_modules']
        },
        'react': {
            'extensions': ['.jsx', '.tsx'],
            'files': ['package.json'],  # Check for react dependency
            'patterns': ['react', 'next.js', 'create-react-app']
        },
        'vue': {
            'extensions': ['.vue'],
            'files': ['package.json'],  # Check for vue dependency
            'patterns': ['vue']
        },
        'go': {
            'extensions': ['.go'],
            'files': ['go.mod', 'go.sum'],
            'dirs': []
        },
        'rust': {
            'extensions': ['.rs'],
            'files': ['Cargo.toml', 'Cargo.lock'],
            'dirs': ['target']
        },
        'java': {
            'extensions': ['.java'],
            'files': ['pom.xml', 'build.gradle', 'gradlew'],
            'dirs': ['src/main/java']
        },
        'ruby': {
            'extensions': ['.rb'],
            'files': ['Gemfile', 'Rakefile'],
            'dirs': []
        },
        'php': {
            'extensions': ['.php'],
            'files': ['composer.json', 'composer.lock'],
            'dirs': ['vendor']
        }
    }

    # Framework-specific patterns in package.json
    FRAMEWORK_PATTERNS = {
        'react': ['react', 'react-dom', 'next'],
        'vue': ['vue', 'nuxt'],
        'angular': ['@angular/core'],
        'svelte': ['svelte'],
        'fastapi': ['fastapi', 'uvicorn'],
        'django': ['django'],
        'flask': ['flask'],
        'express': ['express'],
        'nest': ['@nestjs/core']
    }

    def __init__(self, project_dir: str = '.'):
        """Initialize detector with project directory."""
        self.project_dir = Path(project_dir).resolve()

    def detect_languages(self, max_depth: int = 3) -> Set[str]:
        """
        Detect languages used in project.

        Args:
            max_depth: Maximum directory depth to scan

        Returns:
            Set of detected language names
        """
        detected = set()

        # Check for indicator files in root
        for lang, indicators in self.LANGUAGE_INDICATORS.items():
            for indicator_file in indicators.get('files', []):
                if (self.project_dir / indicator_file).exists():
                    detected.add(lang)

        # Scan for source files (limited depth)
        for root, dirs, files in os.walk(self.project_dir):
            # Calculate depth
            depth = len(Path(root).relative_to(self.project_dir).parts)
            if depth > max_depth:
                continue

            # Skip common ignore directories
            dirs[:] = [d for d in dirs if d not in {
                'node_modules', 'venv', '.venv', 'dist', 'build',
                '.git', '__pycache__', 'target', 'vendor'
            }]

            # Check file extensions
            for file in files:
                ext = Path(file).suffix
                for lang, indicators in self.LANGUAGE_INDICATORS.items():
                    if ext in indicators.get('extensions', []):
                        detected.add(lang)

        return detected

    def detect_frameworks(self) -> Set[str]:
        """
        Detect frameworks used in project.

        Returns:
            Set of detected framework names
        """
        detected = set()

        # Check package.json for JavaScript frameworks
        package_json = self.project_dir / 'package.json'
        if package_json.exists():
            try:
                with open(package_json) as f:
                    data = json.load(f)
                    deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}

                    for framework, patterns in self.FRAMEWORK_PATTERNS.items():
                        if any(pattern in deps for pattern in patterns):
                            detected.add(framework)
            except (json.JSONDecodeError, IOError):
                pass

        # Check Python frameworks
        requirements_files = ['requirements.txt', 'pyproject.toml']
        for req_file in requirements_files:
            req_path = self.project_dir / req_file
            if req_path.exists():
                try:
                    content = req_path.read_text().lower()
                    for framework in ['fastapi', 'django', 'flask']:
                        if framework in content:
                            detected.add(framework)
                except IOError:
                    pass

        return detected

    def get_relevant_extensions(self) -> List[str]:
        """
        Get list of relevant file extensions based on detected languages.

        Returns:
            List of file extensions (e.g., ['.py', '.js', '.tsx'])
        """
        languages = self.detect_languages()
        extensions = []

        for lang in languages:
            if lang in self.LANGUAGE_INDICATORS:
                extensions.extend(self.LANGUAGE_INDICATORS[lang].get('extensions', []))

        return list(set(extensions))  # Remove duplicates

    def detect_context(self) -> Dict[str, any]:
        """
        Detect full project context.

        Returns:
            Dictionary with detected languages, frameworks, and extensions
        """
        languages = self.detect_languages()
        frameworks = self.detect_frameworks()
        extensions = self.get_relevant_extensions()

        return {
            'languages': sorted(list(languages)),
            'frameworks': sorted(list(frameworks)),
            'extensions': sorted(extensions),
            'context_string': ', '.join(sorted(list(languages | frameworks)))
        }


def main():
    """CLI entry point for context detection."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Detect languages and frameworks in current project',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--dir', default='.', help='Project directory to analyze (default: current)')
    parser.add_argument('--extensions-only', action='store_true', help='Output only file extensions')

    args = parser.parse_args()

    detector = ProjectContextDetector(args.dir)

    if args.extensions_only:
        extensions = detector.get_relevant_extensions()
        print(','.join(extensions))
    else:
        context = detector.detect_context()
        print(json.dumps(context, indent=2))


if __name__ == '__main__':
    main()
