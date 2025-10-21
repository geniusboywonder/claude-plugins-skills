# Claude Plugins & Skills Marketplace

A curated collection of Claude Code plugins and skills to enhance your development workflows. This marketplace provides ready-to-use extensions for code analysis, repository exploration, and development automation.

## What's Inside

### Plugins

Comprehensive extension packages containing custom commands, agents, skills, and integrations:

- **[github-reader](./plugins/github-reader/)** - Read and analyze public GitHub repositories without cloning

### Skills

Standalone skill packages for specialized agent capabilities:

- **[github-reader](./skills/github-reader/)** - Read and analyze public GitHub repositories without cloning (standalone skill)

## Quick Start

### Installation Methods

#### Method 1: Add as Marketplace (Recommended)

Install plugins directly from this marketplace in Claude Code:

**Using CLI:**
```bash
# Add marketplace via command
/plugin marketplace add geniusboywonder/claude-plugins-skills

# Install plugin from marketplace
/plugin install github-reader
```

**Using Settings File:**

Add to `~/.claude/settings.json`:
```json
{
  "extraKnownMarketplaces": {
    "neill-plugins": {
      "source": {
        "source": "github",
        "repo": "geniusboywonder/claude-plugins-skills"
      }
    }
  }
}
```

Then use `/plugin install github-reader` to install any plugin from this marketplace.

#### Method 2: Individual Plugin Installation

Clone and install specific plugins:

```bash
# Clone the repository
git clone https://github.com/geniusboywonder/claude-plugins-skills.git

# Install a specific plugin
cp -r claude-plugins-skills/plugins/github-reader ~/.claude/plugins/

# OR install as standalone skill
cp -r claude-plugins-skills/skills/github-reader ~/.claude/skills/

# Restart Claude Code or reload plugins
```

#### Method 3: From Release Assets

Download pre-packaged plugins from [Releases](https://github.com/geniusboywonder/claude-plugins-skills/releases):

```bash
# Download and extract
unzip github-reader-v1.0.0.zip -d ~/.claude/plugins/
```

## Available Plugins

### GitHub Reader

**Version:** 1.0.0
**Category:** Development Tools
**Status:** ✅ Stable

Read and analyze public GitHub repositories using an API-first approach without cloning. Features context-aware filtering, automatic example prioritization, and zero disk footprint.
Token optimised for minimal token use.

**Key Features:**
- Zero disk usage - API-first approach
- Context-aware filtering for relevant examples
- Automatic example prioritization
- Progressive disclosure for token efficiency
- No authentication required for public repos

**Installation:**
```bash
# As plugin (full package)
cp -r plugins/github-reader ~/.claude/plugins/

# As standalone skill
cp -r skills/github-reader ~/.claude/skills/
```

[📚 Plugin Documentation](./plugins/github-reader/README.md) | [📚 Skill Documentation](./skills/github-reader/README.md)

**Available As:**
- 📦 Plugin - Full package with plugin wrapper
- ⚡ Skill - Lightweight standalone skill

## Directory Structure

```
claude-plugins-skills/
├── .claude-plugin/
│   └── marketplace.json        # Marketplace catalog
├── plugins/
│   └── github-reader/          # Full plugin package
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   └── github-reader/  # Skill bundled in plugin
│       ├── README.md
│       ├── LICENSE
│       └── CHANGELOG.md
├── skills/
│   └── github-reader/          # Standalone skill option
│       ├── SKILL.md
│       ├── scripts/
│       ├── references/
│       └── README.md
├── README.md                   # This file
├── MARKETPLACE.md              # Marketplace usage guide
├── CONTRIBUTING.md
└── LICENSE
```

## Marketplace Usage

This repository is configured as a Claude Code marketplace. For detailed instructions on using the marketplace, see [MARKETPLACE.md](./MARKETPLACE.md).

**Quick Start:**
```bash
# Add marketplace
/plugin marketplace add geniusboywonder/claude-plugins-skills

# Install plugin
/plugin install github-reader
```

## Contributing

Contributions are welcome! Whether you want to:
- Add a new plugin or skill
- Improve existing plugins
- Fix bugs or add features
- Enhance documentation

Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Adding Your Plugin

1. Fork this repository
2. Create a new directory under `plugins/your-plugin-name/`
3. Add `.claude-plugin/plugin.json` manifest
4. Update `.claude-plugin/marketplace.json` to include your plugin
5. Add comprehensive README and documentation
6. Submit a pull request

## Requirements

- Claude Code (latest version recommended)
- Python 3.8+ (for Python-based plugins)
- Internet connection for API-based plugins

## License

This marketplace and all plugins are licensed under the MIT License - see [LICENSE](LICENSE) file for details.

Individual plugins may have additional licensing terms - check plugin-specific LICENSE files.

## Support

- **Issues:** [GitHub Issues](https://github.com/geniusboywonder/claude-plugins-skills/issues)
- **Discussions:** [GitHub Discussions](https://github.com/geniusboywonder/claude-plugins-skills/discussions)
- **Contributing:** See [CONTRIBUTING.md](./CONTRIBUTING.md)

## Roadmap

### Upcoming Plugins
- [ ] Anything I find useful

### Upcoming Skills
- [ ] Anything I find useful

Want to contribute to the roadmap? Open an issue or discussion!

## Author

**Neill Adamson**
GitHub: [@geniusboywonder](https://github.com/geniusboywonder)

## Version

Marketplace Version: 1.0.0

## Acknowledgments

Built for the Claude Code community. Special thanks to:
- Anthropic for creating Claude Code
- All contributors and plugin authors
- The open-source community

---

**Star this repository** if you find it useful! 🌟
