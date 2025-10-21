# Using the Claude Plugins & Skills Marketplace

This repository is configured as a Claude Code marketplace, allowing you to install plugins directly through Claude Code's plugin management system.

## Adding the Marketplace

### Option 1: CLI Command (Easiest)

```bash
# Add this marketplace to Claude Code
/plugin marketplace add geniusboywonder/claude-plugins-skills
```

### Option 2: Settings File

Edit `~/.claude/settings.json`:

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

## Installing Plugins from Marketplace

Once the marketplace is added:

```bash
# List available plugins from this marketplace
/plugin marketplace list

# Install a specific plugin
/plugin install github-reader

# Update a plugin
/plugin update github-reader

# Uninstall a plugin
/plugin uninstall github-reader
```

## Available Plugins

### github-reader v1.0.0

Read and analyze public GitHub repositories using API-first approach.

**Install:**
```bash
/plugin install github-reader
```

**Features:**
- Zero disk usage - API-first approach
- Context-aware filtering for relevant examples
- Automatic example prioritization
- Progressive disclosure for token efficiency
- No authentication required for public repos

**Documentation:** [GitHub Reader Plugin](./plugins/github-reader/README.md)

## Marketplace Configuration

This repository uses `.claude-plugin/marketplace.json` to define available plugins:

```json
{
  "name": "claude-plugins-skills",
  "owner": {
    "name": "Neill Adamson",
    "email": "nadamson@gmail.com",
    "github": "geniusboywonder"
  },
  "plugins": [
    {
      "name": "github-reader",
      "source": {
        "source": "github",
        "repo": "geniusboywonder/claude-plugins-skills",
        "path": "plugins/github-reader"
      },
      "version": "1.0.0",
      "description": "Read and analyze public GitHub repositories",
      "category": "development-tools"
    }
  ]
}
```

## How It Works

1. **Marketplace Discovery**: Claude Code reads `.claude-plugin/marketplace.json` from this repository
2. **Plugin Sources**: Each plugin specifies a GitHub source path
3. **Installation**: Claude Code fetches the plugin from the specified path
4. **Updates**: Plugin versions are tracked for update notifications

## For Plugin Authors

Want to add your plugin to this marketplace? See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on:
- Plugin structure requirements
- Manifest format
- Documentation standards
- Submission process

## Troubleshooting

### Marketplace Not Found

Ensure the repository path is correct:
```bash
/plugin marketplace add geniusboywonder/claude-plugins-skills
```

### Plugin Installation Fails

Check that:
- The plugin name matches exactly (case-sensitive)
- Your Claude Code version is up to date
- You have internet connectivity

### Updates Not Working

Try removing and re-adding the marketplace:
```bash
/plugin marketplace remove neill-plugins
/plugin marketplace add geniusboywonder/claude-plugins-skills
```

## Support

- **Issues**: [GitHub Issues](https://github.com/geniusboywonder/claude-plugins-skills/issues)
- **Discussions**: [GitHub Discussions](https://github.com/geniusboywonder/claude-plugins-skills/discussions)
- **Documentation**: [Main README](./README.md)
