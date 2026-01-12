@echo off
REM Quick setup script for VS Code extension development (Windows)

echo.
echo 🚀 HeyGen MCP VS Code Extension - Setup Script
echo ================================================
echo.

REM Check if we're in the right directory
if not exist "package.json" (
    echo ❌ Error: package.json not found!
    echo Please run this script from the vscode-extension directory
    exit /b 1
)

echo 📦 Installing dependencies...
call npm install
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    exit /b 1
)
echo ✅ Dependencies installed
echo.

echo 🔨 Building extension...
call npm run esbuild
if errorlevel 1 (
    echo ❌ Failed to build extension
    exit /b 1
)
echo ✅ Extension built successfully
echo.

echo 📝 Next steps:
echo 1. Press F5 to launch the extension in debug mode
echo 2. Test the extension in the new VS Code window
echo 3. Configure your HeyGen API key using the command palette
echo 4. Try asking your AI assistant to generate a video
echo.

echo 📚 For more information, see:
echo    - README.md - User documentation
echo    - QUICKSTART.md - Quick reference
echo    - DEVELOPMENT.md - Development guide
echo    - ARCHITECTURE.md - Technical details
echo.

echo ✨ Ready to develop!
