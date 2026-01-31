# Release Process

This document describes how to create releases for the HeyGen MCP project.

## Overview

A single Git tag (`v*`) triggers both release workflows:
- **Python Package** → Publishes to PyPI
- **VS Code Extension** → Publishes to VS Code Marketplace

Both artifacts are uploaded to the same GitHub release.

## ⚠️ Important: Do NOT manually update version numbers

The CI workflows automatically update version numbers based on the tag. **Do NOT** manually edit:
- `pyproject.toml` version
- `vscode-extension/package.json` version

## Creating a Release

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

3. **The release workflows will automatically:**
   - Update version in `pyproject.toml` and `vscode-extension/package.json`
   - Build the Python package and publish to PyPI
   - Build the VS Code extension and publish to Marketplace
   - Create a single GitHub release with both artifacts

### Version Format
- Use semantic versioning: `vMAJOR.MINOR.PATCH`
- Examples: `v0.3.0`, `v1.0.0`, `v2.1.3`

## Fixing Failed Releases

If a release workflow fails:

1. **Delete the tag locally and remotely**
   ```bash
   git tag -d v0.3.1
   git push origin :refs/tags/v0.3.1
   ```

2. **Delete the GitHub release** (if created)
   ```bash
   gh release delete v0.3.1 --yes
   ```

3. **Fix the issue and push to main**

4. **Re-create and push the tag**
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
- `PYPI_API_TOKEN` - For publishing to PyPI (or use trusted publishing)
- `VSCE_TOKEN` - For publishing to VS Code Marketplace
