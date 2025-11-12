@echo off
REM Auralis Quick Start Script for Windows
REM Automatically sets up the entire MVP environment

echo ========================================
echo    Auralis MVP Quick Start (Windows)
echo ========================================
echo.

REM Check prerequisites
echo Checking prerequisites...

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found. Please install Python 3.10+
    exit /b 1
)

where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js not found. Please install Node.js 18+
    exit /b 1
)

where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] npm not found. Please install npm
    exit /b 1
)

echo [OK] Prerequisites check passed
echo.

REM Backend setup
echo Setting up backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -q -r requirements.txt

echo [OK] Backend setup complete
echo.

REM Optional: Install Slither
set /p INSTALL_SLITHER="Install Slither for static analysis? (y/n): "
if /i "%INSTALL_SLITHER%"=="y" (
    echo Installing Slither...
    call ..\tools\install_slither.bat
    echo [OK] Slither installed
)
echo.

REM Start backend
echo Starting backend server...
start /b python -m uvicorn main:app --host 0.0.0.0 --port 8000

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

REM Check if backend is running
curl -s http://localhost:8000/health >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Backend is running at http://localhost:8000
) else (
    echo [ERROR] Backend failed to start
    exit /b 1
)

cd ..
echo.

REM VS Code extension setup
echo Setting up VS Code extension...
cd vscode-extension

echo Installing npm dependencies...
call npm install

echo Compiling TypeScript...
call npm run compile

echo Packaging extension...
call npm run package

echo [OK] VS Code extension packaged: auralis-vscode-0.1.0.vsix
cd ..
echo.

REM Summary
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Install VS Code extension:
echo    - Open VS Code
echo    - Extensions -^> ... -^> Install from VSIX
echo    - Select: vscode-extension\auralis-vscode-0.1.0.vsix
echo.
echo 2. Configure VS Code settings:
echo    {
echo      "auralis.apiEndpoint": "http://localhost:8000",
echo      "auralis.enableRealTimeAnalysis": true
echo    }
echo.
echo 3. Test the extension:
echo    - Open a .sol file
echo    - Save to trigger analysis
echo    - View results in Problems panel
echo.
echo 4. Backend is running at: http://localhost:8000
echo    - Health check: http://localhost:8000/health
echo    - API docs: http://localhost:8000/docs
echo.
echo 5. To stop backend:
echo    - Close this window or press Ctrl+C
echo.
echo Read MVP_README.md for detailed usage instructions
echo Read DEMO_INSTRUCTIONS.md for demo setup
echo.
echo Happy auditing!
echo.
pause
