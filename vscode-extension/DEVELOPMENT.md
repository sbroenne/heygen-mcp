# VS Code Extension Development

This directory contains the VS Code extension for the HeyGen MCP server.

## Quick Start

### Install Dependencies

```bash
npm install
```

### Build

```bash
npm run esbuild
```

### Develop with Watch Mode

```bash
npm run esbuild-watch
```

### Debug

Press `F5` to launch the extension in debug mode. The extension will run in a new VS Code window where you can test it.

### Package

```bash
npm install -g vsce
vsce package
```

## Structure

```
vscode-extension/
├── src/
│   └── extension.ts       # Main extension code
├── .vscode/
│   └── launch.json        # Debug configuration
├── package.json           # Extension manifest
├── tsconfig.json          # TypeScript configuration
└── README.md              # User-facing documentation
```

## Key Features

- **MCP Server Registration**: Registers the HeyGen MCP server with VS Code
- **API Key Management**: Secure handling of HeyGen API keys
- **Auto-initialization**: Automatically prompts for API key on first use
- **Commands**: Quick access commands for configuration and help
- **Settings Integration**: VS Code settings integration for easy configuration

## API

The extension registers:

1. **MCP Server Definition Provider**: `heygen-mcp.provider`
2. **Commands**:
   - `heygen-mcp.configure` - Configure API key
   - `heygen-mcp.help` - Show help information

3. **Settings**:
   - `heygen-mcp.apiKey` - API key (workspace-level for security)
   - `heygen-mcp.autoStartServer` - Auto-start on VS Code launch

## Publishing

To publish to the VS Code Marketplace:

```bash
npm run esbuild-base -- --minify
vsce publish
```

Requires:
- VS Code Marketplace account
- `vsce` CLI (`npm install -g vsce`)
- Increment version in `package.json`
