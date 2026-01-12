# HeyGen MCP Server - VS Code Extension

HeyGen MCP Server for VS Code, enabling AI assistants like GitHub Copilot to generate videos, manage avatars, templates, and more through the Model Context Protocol.

## Features

- **Video Generation**: Create AI avatar videos with custom text and voices
- **Avatar IV Support**: Generate photorealistic videos from photos
- **Template Management**: Work with dynamic templates and variables
- **Asset Management**: Upload and manage media files (images, videos, audio)
- **Folder Organization**: Organize your videos and templates
- **Avatar & Voice Selection**: Access all available avatars and voices
- **Seamless Integration**: Works with VS Code's language model features and Copilot

## Requirements

- **VS Code 1.106.0** or later
- **[uv](https://docs.astral.sh/uv/)** - The extension uses `uvx` to run the MCP server
  - macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows: `irm https://astral.sh/uv/install.ps1 | iex`
  - See [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) for more options
- **HeyGen API key** - [Get one here](https://app.heygen.com/settings?nav=API) (10 free credits/month)

## Installation

### From VS Code Marketplace

- [Install from VS Code Marketplace →](https://marketplace.visualstudio.com/items?itemName=sbroenne.heygen-mcp)
- Or search for "sbroenne.heygen-mcp" in VS Code Extensions (Ctrl+Shift+X)

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sbroenne/heygen-mcp.git
   cd heygen-mcp/vscode-extension
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Build the extension:
   ```bash
   npm run esbuild
   ```

4. Package the extension:
   ```bash
   npx vsce package
   ```

5. Install the `.vsix` file in VS Code (Extensions → Install from VSIX)

## Configuration

### 1. Get Your HeyGen API Key

1. Sign up at [HeyGen](https://www.heygen.com/)
2. Go to your dashboard and create an API key
3. Copy the API key

### 2. Configure in VS Code

The extension will prompt for your API key on first use. You can also:

1. Use Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
2. Search for "HeyGen: Configure API Key"
3. Enter your API key when prompted

Or manually in settings (File → Preferences → Settings → search for "heygen"):

- **heygen-mcp.apiKey**: Your HeyGen API key

## Usage

Once configured, the HeyGen MCP server will automatically be available to:

- Claude in VS Code
- GitHub Copilot (with MCP support)
- Other AI assistants that support MCP

Ask your AI assistant to:

```
Generate an avatar video with...
Create a video from a template...
Upload an image to HeyGen...
List my avatars and voices...
```

## Available MCP Tools

The extension provides access to these HeyGen tools:

### User
- Get user profile information
- Check remaining credits

### Voices
- List available voices for video generation

### Avatars
- List all avatars
- Get avatar details
- List avatar groups
- Get avatars in a specific group

### Videos
- Generate avatar videos
- Create Avatar IV videos from photos
- Check video processing status

### Templates
- List templates
- Get template details with variables
- Generate videos from templates

### Assets
- Upload media files (images, videos, audio)
- List assets
- Delete assets

### Folders
- List folders
- Create folders
- Rename folders
- Organize with folder hierarchy

## Requirements

- VS Code 1.106.0 or later
- Python 3.10+ with `heygen-mcp-sbroenne` package installed
- HeyGen API key (free tier available with monthly credits)

## Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `heygen-mcp.apiKey` | string | - | Your HeyGen API key (required) |
| `heygen-mcp.autoStartServer` | boolean | true | Automatically start the server on VS Code startup |

## Development

### Prerequisites

- Node.js 16+ (for building the extension)
- VS Code 1.106.0+
- npm

### Setup

```bash
cd vscode-extension
npm install
```

### Build

```bash
npm run esbuild
```

### Watch Mode

```bash
npm run esbuild-watch
```

### Run Extension

Press `F5` or go to Run and Debug to launch the extension in a development host.

### Debug

Set breakpoints and use VS Code's debugging tools to debug the extension.

## Publishing

To publish a new version:

1. Update version in `package.json`
2. Build and package:
   ```bash
   npm run vscode:prepublish
   npx vsce package
   ```
3. Publish to VS Code Marketplace:
   ```bash
   npx vsce publish
   ```

## Troubleshooting

### "HeyGen MCP server not found" or "uvx command not found"

Make sure `uv` is installed (see [Requirements](#requirements) above). After installing, restart VS Code.

### "API key not valid"

1. Verify your API key at [HeyGen Dashboard](https://app.heygen.com/settings?nav=API)
2. Use "HeyGen: Configure API Key" command to update it
3. The key is saved in VS Code's global settings

### Extension not activating

1. Reload VS Code window (Ctrl+Shift+P → "Developer: Reload Window")
2. Check VS Code output for errors (View → Output → select "HeyGen MCP" from dropdown)

## Links

- [HeyGen](https://www.heygen.com/)
- [HeyGen API Documentation](https://docs.heygen.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [GitHub Repository](https://github.com/sbroenne/heygen-mcp)

## License

MIT - See LICENSE file for details

## Support

For issues and feature requests, visit:
https://github.com/sbroenne/heygen-mcp/issues

## Contributing

Contributions welcome! See the main repository for contribution guidelines.
