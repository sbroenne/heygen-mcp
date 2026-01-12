# VS Code Extension Summary

## Overview

The HeyGen MCP Server for VS Code, enabling seamless video generation, avatar management, and template operations directly from your AI assistant through the Model Context Protocol.

## Created Files

```
vscode-extension/
├── package.json              # Extension manifest with MCP provider definition
├── tsconfig.json             # TypeScript compiler configuration
├── .eslintrc.json            # ESLint configuration
├── .vscodeignore             # Files to exclude from extension package
├── .gitignore                # Git ignore rules
├── README.md                 # User-facing documentation
├── DEVELOPMENT.md            # Development guide
├── src/
│   └── extension.ts          # Main extension code
└── .vscode/
    └── launch.json           # Debug configuration
```

## Key Features

### 1. **MCP Server Registration**
- Registers HeyGen MCP server as an MCP server definition provider
- VS Code automatically makes the server available to language models
- Works with Claude in VS Code, GitHub Copilot, and other MCP-compatible assistants

### 2. **API Key Management**
- Prompts for API key on first use
- Saves key to workspace settings (not global for security)
- Command palette support for reconfiguring API key
- Validates API key before starting server

### 3. **Automatic Initialization**
- Activates on VS Code startup
- Checks for configured API key
- Prompts user if needed
- Gracefully handles missing configuration

### 4. **VS Code Commands**
- `heygen-mcp.configure` - Configure or update API key
- `heygen-mcp.help` - Show help and quick links

### 5. **Settings Integration**
- `heygen-mcp.apiKey` - API key (workspace-level)
- `heygen-mcp.autoStartServer` - Auto-start on launch (default: true)

## How It Works

1. **Installation**: User installs the extension from VS Code Marketplace
2. **Activation**: Extension activates on VS Code startup
3. **Configuration**: Extension prompts for HeyGen API key if not configured
4. **Registration**: Extension registers the HeyGen MCP server with VS Code
5. **Integration**: VS Code makes the server available to language models
6. **Usage**: User can ask AI assistant to generate videos, manage templates, etc.

## File Descriptions

### `package.json`
- Defines extension metadata (name, version, publisher)
- Lists dependencies (VS Code API types, TypeScript, esbuild)
- Defines `mcpServerDefinitionProviders` contribution point
- Specifies build scripts (esbuild, TypeScript, ESLint)
- Configures extension settings schema

### `src/extension.ts`
- **`activate()`**: Called when extension is loaded
  - Registers MCP server definition provider
  - Registers VS Code commands (configure, help)
  - Sets up event listeners for configuration changes

- **`provideMcpServerDefinitions()`**: Provides the server to VS Code
  - Checks for configured API key
  - Returns stdio server definition if key exists
  - Returns empty array if no key configured

- **`resolveMcpServerDefinition()`**: Called when server is about to start
  - Prompts for API key if not configured
  - Updates workspace settings with new key
  - Triggers re-evaluation to restart server

- **Commands**:
  - `heygen-mcp.configure`: Manage API key interactively
  - `heygen-mcp.help`: Show help and links

### `tsconfig.json`
- TypeScript compiler options
- Targets ES2020 with CommonJS modules
- Strict type checking enabled
- Output to `./out` directory

### `.vscode/launch.json`
- Debug configuration for F5 debugging
- Launches extension in a new VS Code window
- Enables source maps for debugging

### `README.md`
- User-facing documentation
- Installation instructions
- Configuration guide
- Feature list
- Troubleshooting section
- Links to resources

## Building and Publishing

### Local Development

```bash
# Install dependencies
cd vscode-extension
npm install

# Build
npm run esbuild

# Watch mode
npm run esbuild-watch

# Debug (F5)
```

### Publish to VS Code Marketplace

```bash
# Build release version
npm run vscode:prepublish

# Package extension
vsce package

# Publish
vsce publish
```

## Architecture

```
┌─────────────────────────────────────────┐
│           VS Code Window                │
├─────────────────────────────────────────┤
│    HeyGen MCP Extension                 │
│  ┌────────────────────────────────────┐ │
│  │ MCP Server Definition Provider    │ │
│  │ - Provides server to VS Code      │ │
│  │ - Manages API key                 │ │
│  │ - Registers commands              │ │
│  └────────────────────────────────────┘ │
└────────────────┬────────────────────────┘
                 │
                 │ stdio
                 ▼
         ┌─────────────────┐
         │ HeyGen MCP Server│
         │  (heygen-mcp)    │
         └────────┬─────────┘
                  │ HTTPS
                  ▼
         ┌─────────────────┐
         │  HeyGen API     │
         │ (api.heygen.com)│
         └─────────────────┘
```

## Configuration Flow

```
Extension Activated
       │
       ▼
Has API Key?
    /        \
  Yes        No
   │          │
   │          ▼
   │    Prompt User
   │    ┌─────────┐
   │    │ Enter   │
   │    │ API Key │
   │    └────┬────┘
   │         │
   │         ▼
   │    Save to Settings
   └────┬────────────────┘
        │
        ▼
Register MCP Server Provider
        │
        ▼
Server Available to Language Models
```

## Security Considerations

- API key stored in workspace settings (not global)
- No API key logging in console
- Password input masks API key entry
- Server only starts if API key is configured
- Validation before server initialization

## Requirements

- VS Code 1.106.0+
- Node.js 16+ (for development)
- HeyGen API key (from https://www.heygen.com)

## Next Steps

1. Install npm dependencies: `npm install`
2. Build extension: `npm run esbuild`
3. Debug with F5 in VS Code
4. Test MCP server integration
5. Publish to VS Code Marketplace when ready

## Support

- GitHub: https://github.com/sbroenne/heygen-mcp
- Issues: https://github.com/sbroenne/heygen-mcp/issues
- HeyGen: https://www.heygen.com/
