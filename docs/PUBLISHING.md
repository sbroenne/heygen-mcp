# PyPI Publishing Guide

This guide explains how to set up and publish `heygen-mcp-sbroenne` to PyPI using GitHub Actions with trusted publishing (OIDC).

## Prerequisites

- A [PyPI account](https://pypi.org/account/register/)
- A [TestPyPI account](https://test.pypi.org/account/register/) (recommended, uses separate credentials)
- Repository owner/admin access to `sbroenne/heygen-mcp`

## Step 1: Configure Trusted Publishing on PyPI

Trusted publishing uses OpenID Connect (OIDC) - no API tokens needed!

### TestPyPI Setup

1. Go to https://test.pypi.org/manage/account/publishing/
2. Scroll to "Add a new pending publisher"
3. Fill in the form:
   - **PyPI Project Name:** `heygen-mcp-sbroenne`
   - **Owner:** `sbroenne`
   - **Repository name:** `heygen-mcp`
   - **Workflow name:** `release.yml`
   - **Environment name:** `testpypi`
4. Click "Add"

### PyPI Setup

1. Go to https://pypi.org/manage/account/publishing/
2. Scroll to "Add a new pending publisher"
3. Fill in the form:
   - **PyPI Project Name:** `heygen-mcp-sbroenne`
   - **Owner:** `sbroenne`
   - **Repository name:** `heygen-mcp`
   - **Workflow name:** `release.yml`
   - **Environment name:** `pypi`
4. Click "Add"

## Step 2: Create GitHub Environments

1. Go to https://github.com/sbroenne/heygen-mcp/settings/environments
2. Click "New environment"
3. Create environment named: `testpypi`
   - Optionally add protection rules (e.g., required reviewers)
4. Click "New environment" again
5. Create environment named: `pypi`
   - **Recommended:** Add protection rule requiring manual approval for production releases

## Step 3: Release Process

### Prepare the Release

1. Update version in `pyproject.toml`:
   ```toml
   version = "0.1.0"  # Increment as needed
   ```

2. Commit your changes:
   ```bash
   git add -A
   git commit -m "chore: prepare release v0.1.0"
   git push origin main
   ```

### Create and Push Tag

```bash
# Create annotated tag
git tag -a v0.1.0 -m "Release v0.1.0"

# Push tag to trigger release workflow
git push origin v0.1.0
```

### Monitor the Release

1. Go to https://github.com/sbroenne/heygen-mcp/actions
2. Watch the "Release" workflow
3. The workflow will:
   - Build the package
   - Test the built package
   - Publish to TestPyPI
   - Publish to PyPI
   - Create a GitHub Release with artifacts

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

| Version | When to Use |
|---------|-------------|
| `0.1.0` → `0.1.1` | Bug fixes (patch) |
| `0.1.0` → `0.2.0` | New features, backward compatible (minor) |
| `0.1.0` → `1.0.0` | Breaking changes (major) |

For pre-releases:
- `v0.2.0-alpha.1` - Alpha release
- `v0.2.0-beta.1` - Beta release
- `v0.2.0-rc.1` - Release candidate

## Verify Installation

After publishing, verify the package works:

```bash
# From TestPyPI
pip install -i https://test.pypi.org/simple/ heygen-mcp-sbroenne

# From PyPI (production)
pip install heygen-mcp-sbroenne

# Or with uvx
uvx heygen-mcp-sbroenne --help
```

## Troubleshooting

### "Project not found" Error

The pending publisher must be created **before** the first publish. If you already published manually, go to the project settings on PyPI and add the trusted publisher there instead.

### Environment Not Found

Make sure you created the GitHub environments (`testpypi` and `pypi`) exactly as spelled in the workflow file.

### Permission Denied

Ensure the workflow has `id-token: write` permission (already configured in `release.yml`).

### Version Already Exists

PyPI doesn't allow re-uploading the same version. Bump the version number and create a new tag.

## Manual Publishing (Emergency)

If GitHub Actions fails, you can publish manually:

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

You'll need to create API tokens at:
- https://test.pypi.org/manage/account/token/
- https://pypi.org/manage/account/token/
