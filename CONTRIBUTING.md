# Contributing to Claude Plugins & Skills

Thank you for your interest in contributing to the Claude Plugins & Skills marketplace! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Plugin Development Guidelines](#plugin-development-guidelines)
- [Submission Process](#submission-process)
- [Quality Standards](#quality-standards)

## Code of Conduct

This project follows a code of conduct based on respect, inclusivity, and collaboration:

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy towards others

## How Can I Contribute?

### Reporting Bugs

- Use the GitHub issue tracker
- Check if the bug has already been reported
- Provide detailed reproduction steps
- Include environment details (OS, Claude Code version, Python version)

### Suggesting Enhancements

- Open a GitHub discussion for major changes
- Clearly describe the proposed feature
- Explain why it would be useful to the community
- Consider implementation details

### Contributing Code

1. **Bug Fixes** - Submit a PR with a clear description
2. **New Features** - Discuss first via GitHub discussions
3. **New Plugins** - Follow the plugin development guidelines below
4. **Documentation** - Improvements are always welcome

## Plugin Development Guidelines

### Plugin Structure

Every plugin must follow this structure:

```
your-plugin/
├── .claude-plugin/
│   └── plugin.json              # Required: Plugin manifest
├── skills/                      # Optional: Skills directory
│   └── your-skill/
│       └── SKILL.md
├── commands/                    # Optional: Custom commands
├── agents/                      # Optional: Custom agents
├── README.md                    # Required: Plugin documentation
├── LICENSE                      # Required: License file
├── CHANGELOG.md                 # Required: Version history
└── .gitignore                   # Recommended
```

### Plugin Manifest (plugin.json)

Required fields:

```json
{
  "name": "your-plugin-name",
  "version": "1.0.0",
  "description": "Clear, concise description",
  "author": {
    "name": "Your Name"
  },
  "homepage": "https://github.com/geniusboywonder/claude-plugins-skills/tree/main/plugins/your-plugin",
  "repository": {
    "type": "git",
    "url": "https://github.com/geniusboywonder/claude-plugins-skills.git",
    "directory": "plugins/your-plugin"
  },
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "category": "development-tools"
}
```

Optional but recommended fields:
- `tags`: Array of tags for searchability
- `requirements`: System/language requirements
- `metadata`: Additional plugin metadata

### README Requirements

Every plugin must have a comprehensive README including:

1. **Overview** - What the plugin does
2. **Installation** - Step-by-step installation instructions
3. **Features** - Key capabilities
4. **Usage** - Examples and use cases
5. **Requirements** - Dependencies and system requirements
6. **Limitations** - Known limitations
7. **License** - License information
8. **Author** - Author/maintainer information

### Code Quality Standards

- **Python code:**
  - Python 3.8+ compatibility
  - Follow PEP 8 style guide
  - Include docstrings for functions/classes
  - Handle errors gracefully
  - No external dependencies unless necessary (or clearly documented)

- **Documentation:**
  - Clear and concise
  - Include code examples
  - Explain key concepts
  - Provide troubleshooting guidance

- **Testing:**
  - Include test cases when applicable
  - Document testing procedures
  - Ensure cross-platform compatibility

### Versioning

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality (backwards compatible)
- **PATCH** version for bug fixes

### Changelog

Maintain a CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [1.0.0] - 2025-10-21

### Added
- New feature description

### Changed
- Changed feature description

### Fixed
- Bug fix description
```

## Submission Process

### Adding a New Plugin

1. **Fork the repository**
   ```bash
   gh repo fork geniusboywonder/claude-plugins-skills
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b plugin/your-plugin-name
   ```

3. **Create plugin structure**
   ```bash
   mkdir -p plugins/your-plugin/{.claude-plugin,skills}
   ```

4. **Develop your plugin**
   - Add plugin.json manifest
   - Create README.md
   - Add LICENSE file
   - Create CHANGELOG.md
   - Implement functionality

5. **Update marketplace.json**
   Add your plugin to `.claude-plugin/marketplace.json`:
   ```json
   {
     "name": "your-plugin-name",
     "source": "./your-plugin",
     "description": "Brief description",
     "version": "1.0.0",
     "author": {
       "name": "Your Name"
     },
     "category": "development-tools",
     "tags": ["tag1", "tag2"]
   }
   ```

6. **Test thoroughly**
   - Install plugin locally
   - Test all features
   - Verify documentation accuracy
   - Check cross-platform compatibility (if applicable)

7. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: Add your-plugin-name plugin"
   git push origin plugin/your-plugin-name
   ```

8. **Create pull request**
   - Clear title: "Add [Plugin Name] plugin"
   - Detailed description of functionality
   - Screenshots/examples if applicable
   - Checklist of completed requirements

### Pull Request Checklist

Before submitting, ensure:

- [ ] Plugin follows directory structure guidelines
- [ ] `plugin.json` has all required fields
- [ ] README.md is comprehensive
- [ ] LICENSE file is included (MIT recommended)
- [ ] CHANGELOG.md documents version history
- [ ] `.claude-plugin/marketplace.json` updated
- [ ] Code follows quality standards
- [ ] Plugin tested locally
- [ ] No sensitive data (API keys, credentials) included
- [ ] `.gitignore` excludes build artifacts and cache files

## Quality Standards

### Documentation
- Clear, concise language
- Proper markdown formatting
- Code examples with syntax highlighting
- Troubleshooting section

### Code
- Clean, readable code
- Appropriate comments
- Error handling
- No hardcoded credentials
- Minimal dependencies

### Testing
- Manual testing completed
- Edge cases considered
- Cross-platform compatibility (when applicable)

### Security
- No credentials in code
- Input validation
- Safe API usage
- Security best practices

## Review Process

1. **Initial Review** - Automated checks and basic validation
2. **Code Review** - Manual review by maintainers
3. **Testing** - Functionality verification
4. **Documentation Review** - Clarity and completeness
5. **Approval** - Merge when all requirements met

Typical review time: 3-7 days

## Categories

Plugins should be categorized appropriately:

- `development-tools` - Code analysis, generation, refactoring
- `testing` - Test generation, automation, validation
- `documentation` - Documentation generation, analysis
- `security` - Security scanning, vulnerability detection
- `performance` - Performance analysis, optimization
- `integration` - External service integrations
- `utilities` - General utility tools
- `ai-assistants` - AI-powered assistants and agents

## Questions?

- Open a [GitHub Discussion](https://github.com/geniusboywonder/claude-plugins-skills/discussions)
- Check existing [Issues](https://github.com/geniusboywonder/claude-plugins-skills/issues)
- Review this contributing guide

## Recognition

Contributors will be:
- Listed in plugin documentation (if desired)
- Recognized in release notes
- Added to contributors list

Thank you for contributing to Claude Plugins & Skills! 🎉
