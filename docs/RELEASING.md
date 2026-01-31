# Release Process

This document describes how to create releases for the HeyGen MCP project.

## Overview

The project has two release workflows triggered by Git tags:
- **Python Package** (`v*` tags) → Publishes to PyPI
- **VS Code Extension** (`vscode-v*` tags) → Publishes to VS Code Marketplace

## ⚠️ Important: Do NOT manually update version numbers

The CI workflows automatically update version numbers based on the tag. **Do NOT** manually edit:
- `pyproject.toml` version
- `vscode-extension/package.json` version

## Python Package Release

### Steps

1. **Ensure all changes are merged to `main`**
   ```bash
   git checkout main
   git pull
   ```

2. **Create and push the version tag**
   ```bash
   git tag v0.3.1
   git push origin v0.3.1
   ```

3. **The release workflow will automatically:**
   - Update version in `pyproject.toml`
   - Build the package
   - Publish to PyPI
   - Create a GitHub release

### Version Format
- Use semantic versioning: `vMAJOR.MINOR.PATCH`
- Examples: `v0.3.0`, `v1.0.0`, `v2.1.3`

## VS Code Extension Release

### Steps

1. **Ensure all changes are merged to `main`**
   ```bash
   git checkout main
   git pull
   ```

2. **Create and push the version tag**
   ```bash
   git tag vscode-v0.1.2
   git push origin vscode-v0.1.2
   ```

3. **The release workflow will automatically:**
   - Update version in `vscode-extension/package.json`
   - Build and package the extension
   - Publish to VS Code Marketplace (if VSCE_TOKEN is set)
   - Create a GitHub release with the `.vsix` file

### Version Format
- Use semantic versioning with `vscode-` prefix: `vscode-vMAJOR.MINOR.PATCH`
- Examples: `vscode-v0.1.0`, `vscode-v1.0.0`

## Combined Release

When releasing both Python and VS Code extension:

```bash
git checkout main
git pull

# Create both tags
git tag v0.3.1
git tag vscode-v0.1.2

# Push both tags
git push origin v0.3.1
git push origin vscode-v0.1.2
```

## Fixing Failed Releases

If a release workflow fails:

1. **Delete the tag locally and remotely**
   ```bash
   git tag -d v0.3.1
   git push origin :refs/tags/v0.3.1
   ```

2. **Fix the issue and push to main**

3. **Re-create and push the tag**
   ```bash
   git tag v0.3.1
   git push origin v0.3.1
   ```

## GitHub Release Notes

After the CI creates the release, you can edit the release notes on GitHub:
1. Go to https://github.com/sbroenne/heygen-mcp/releases
2. Click on the release
3. Click "Edit release"
4. Update the description as needed

## Secrets Required

The following GitHub secrets must be configured:
- `PYPI_API_TOKEN` - For publishing to PyPI
- `VSCE_TOKEN` - For publishing to VS Code Marketplace
