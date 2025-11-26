# Heygen MCP Server

![Heygen Logo](heygen_logo.png)

> ⚠️ **Disclaimer**: This is a community fork of the original HeyGen MCP server, which appears to be abandoned. This is **not** an official HeyGen repository. Use at your own discretion.

The HeyGen MCP server enables any MCP Client like Claude Desktop or Agents to use the [HeyGen API](https://docs.heygen.com/) to generate avatars and videos.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Note: This project is in early development. While we welcome community feedback and contributions, please be aware that official support is limited.

## Installation

### Prerequisites

- Python 3.10 or higher
- A Heygen API key (get one from [Heygen](https://www.heygen.com/)). Includes 10 Free Credits per Month

### Installing uv

uv is a fast Python package installer and resolver that we recommend for installing this package.

**macOS or Linux:**

```bash
# Install with the official installer script
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via Homebrew (macOS)
brew install uv
```

**Windows:**

```powershell
# Install with the official installer script in PowerShell
irm https://astral.sh/uv/install.ps1 | iex

# Or via Scoop
scoop install uv
```

For other installation methods, see the [uv documentation](https://github.com/astral-sh/uv).

## Usage

### Quickstart with Claude Desktop

1. Get your API key from [HeyGen](https://www.heygen.com/).
2. Install uv package manager (see [Installing uv](#installing-uv) section above).
3. Go to Claude > Settings > Developer > Edit Config > `claude_desktop_config.json` to include the following:

```json
{
  "inputs": [
    {
      "id": "heygen-api-key",
      "type": "promptString",
      "description": "HeyGen API Key",
      "password": true
    }
  ],
  "mcpServers": {
    "HeyGen": {
      "command": "uvx",
      "args": ["heygen-mcp"],
      "env": {
        "HEYGEN_API_KEY": "${input:heygen-api-key}"
      }
    }
  }
}
```

If you're using Windows, you'll need to enable "Developer Mode" in Claude Desktop to use the MCP server. Click "Help" in the hamburger menu at the top left and select "Enable Developer Mode".

### Using with VS Code

Add the following to your VS Code settings (`.vscode/mcp.json`):

```json
{
  "inputs": [
    {
      "id": "heygen-api-key",
      "type": "promptString",
      "description": "HeyGen API Key",
      "password": true
    }
  ],
  "servers": {
    "HeyGen": {
      "type": "stdio",
      "command": "uvx",
      "args": ["heygen-mcp"],
      "env": {
        "HEYGEN_API_KEY": "${input:heygen-api-key}"
      }
    }
  }
}
```

### Using a Local Development Version

If you want to run from a local clone (for development or testing), use `uv run` instead of `uvx`:

```json
{
  "inputs": [
    {
      "id": "heygen-api-key",
      "type": "promptString",
      "description": "HeyGen API Key",
      "password": true
    },
    {
      "id": "heygen-mcp-path",
      "type": "promptString",
      "description": "Path to local heygen-mcp repository"
    }
  ],
  "mcpServers": {
    "HeyGen": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "${input:heygen-mcp-path}",
        "python",
        "-m",
        "heygen_mcp.server"
      ],
      "env": {
        "HEYGEN_API_KEY": "${input:heygen-api-key}"
      }
    }
  }
}
```

For VS Code, use `servers` instead of `mcpServers`.

### Available MCP Tools

The server provides the following tools to Claude:

#### Credits & User

- **get_remaining_credits**: Retrieves the remaining credits in your HeyGen account.
- **get_user_info**: Retrieves profile information of the currently authenticated HeyGen user.

#### Voices

- **get_voices**: Retrieves a list of available voices from the HeyGen API (limited to first 100 voices).

#### Avatars

- **get_avatar_groups**: Retrieves a list of HeyGen avatar groups (private by default, can include public).
- **get_avatars_in_avatar_group**: Retrieves a list of avatars in a specific HeyGen avatar group.
- **list_avatars**: Retrieves a list of all available avatars and talking photos (Photo Avatars).
- **get_avatar_details**: Retrieves detailed information about a specific avatar by its ID.

#### Video Generation

- **generate_avatar_video**: Generates a new avatar video with the specified avatar, text, and voice.
- **get_avatar_video_status**: Retrieves the status of a video generated via the HeyGen API.

#### Templates

- **list_templates**: Retrieves a list of video templates created under your HeyGen account.
- **get_template_details**: Retrieves detailed information about a specific template including variables.
- **generate_video_from_template**: Generates a video from a template with variable replacements.

#### Assets

- **upload_asset**: Uploads a media file (image, video, or audio) to your HeyGen account.
- **list_assets**: Retrieves a list of all assets in your HeyGen account.
- **delete_asset**: Deletes a specific asset by its asset ID.

## Development

### Running with MCP Inspector

To run the server locally with the MCP Inspector for testing and debugging:

```bash
uv --with "mcp[cli]" dev heygen_mcp/server.py
```

This will start the server in development mode and allow you to use the MCP Inspector to test the available tools and functionality.

## Roadmap

- [x] Tests (integration tests)
- [x] Template API Support
- [ ] CICD
- [ ] Photo Avatar APIs Support
- [ ] SSE And Remote MCP Server with OAuth Flow
- [ ] Translation API Support
- [ ] Interactive Avatar API Support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
