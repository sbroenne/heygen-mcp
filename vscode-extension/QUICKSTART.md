# VS Code Extension Quick Start

## Installation

### From VS Code Marketplace (Recommended)

1. Open VS Code
2. Press `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (macOS)
3. Search for "HeyGen MCP"
4. Click **Install**

### From Source

```bash
cd vscode-extension
npm install
npm run esbuild
vsce package
# Install the generated .vsix file in VS Code
```

## Configuration

### Method 1: Command Palette (Easiest)

1. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
2. Type "HeyGen: Configure API Key"
3. Press Enter
4. Paste your HeyGen API key
5. Done! ✅

### Method 2: Settings

1. Open VS Code Settings (`Ctrl+,`)
2. Search for "heygen-mcp"
3. Paste your API key in the "API Key" field
4. Done! ✅

### Method 3: Workspace Settings

Create or edit `.vscode/settings.json`:

```json
{
  "heygen-mcp": {
    "apiKey": "your-heygen-api-key-here"
  }
}
```

## Getting Your API Key

1. Go to [HeyGen](https://www.heygen.com/)
2. Sign up or log in
3. Navigate to **Settings** → **API Keys**
4. Create or copy your API key
5. Use it in VS Code

## Usage

Once configured, you can ask your AI assistant (Claude, Copilot, etc.):

### Generate Videos
```
Generate an avatar video with the text "Hello, this is my AI avatar" 
using voice ID en-US and avatar jane
```

### Manage Templates
```
List my HeyGen templates
Get the variables for template xyz
Generate a video from my template using variables...
```

### Create Avatar IV Videos
```
Upload a photo and generate an Avatar IV video with motion
```

### Manage Assets
```
Upload an image to HeyGen
List my uploaded assets
Delete an unused asset
```

### Organize Content
```
Create a folder called "Marketing Videos"
Move my videos to the new folder
```

## Verify It Works

1. Open Command Palette (`Ctrl+Shift+P`)
2. Type "HeyGen: Help"
3. You should see the help message
4. If the extension is working, you'll see the HeyGen tools in your AI assistant's context

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Extension not showing up | Reload VS Code (`Ctrl+Shift+P` → "Reload Window") |
| "API key required" | Run "HeyGen: Configure API Key" command |
| "Server not found" | Install `heygen-mcp-sbroenne` package |
| "Connection failed" | Check your internet and HeyGen API status |

## Commands

| Command | Shortcut |
|---------|----------|
| Configure API Key | `Ctrl+Shift+P` → "HeyGen: Configure API Key" |
| Show Help | `Ctrl+Shift+P` → "HeyGen: Help" |

## Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `heygen-mcp.apiKey` | string | - | Your HeyGen API key |
| `heygen-mcp.autoStartServer` | boolean | true | Auto-start server on VS Code launch |

## Tips

✨ **Pro Tips:**

- Your API key is stored in workspace settings for security
- Share workspace settings (`.vscode/settings.json`) with team members
- API key in workspace settings takes precedence over global settings
- Extension activates automatically when VS Code starts
- You can reconfigure your API key anytime

## Getting Help

- 📖 [HeyGen Docs](https://docs.heygen.com/)
- 🐛 [Report Issues](https://github.com/sbroenne/heygen-mcp/issues)
- 💬 [GitHub Discussions](https://github.com/sbroenne/heygen-mcp/discussions)
- 🌐 [HeyGen Support](https://www.heygen.com/)

## What's Next?

1. ✅ Install extension
2. ✅ Configure API key
3. ✅ Reload VS Code
4. ✅ Ask your AI assistant to generate a video
5. 🎉 Enjoy creating AI videos!

---

**Need more help?** See [README.md](README.md) for detailed documentation.
