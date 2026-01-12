#!/bin/bash
# Quick setup script for VS Code extension development

set -e

echo "🚀 HeyGen MCP VS Code Extension - Setup Script"
echo "================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found!"
    echo "Please run this script from the vscode-extension directory"
    exit 1
fi

echo "📦 Installing dependencies..."
npm install
echo "✅ Dependencies installed"
echo ""

echo "🔨 Building extension..."
npm run esbuild
echo "✅ Extension built successfully"
echo ""

echo "📝 Next steps:"
echo "1. Press F5 to launch the extension in debug mode"
echo "2. Test the extension in the new VS Code window"
echo "3. Configure your HeyGen API key using the command palette"
echo "4. Try asking your AI assistant to generate a video"
echo ""

echo "📚 For more information, see:"
echo "   - README.md - User documentation"
echo "   - QUICKSTART.md - Quick reference"
echo "   - DEVELOPMENT.md - Development guide"
echo "   - ARCHITECTURE.md - Technical details"
echo ""

echo "✨ Ready to develop!"
