@echo off
REM Auralis Slither Installation Script for Windows
REM Ensures reproducible Slither environment for development and CI

echo Installing Slither Analyzer...

REM Check Python version
python --version

REM Install Slither
pip install slither-analyzer

REM Verify installation
slither --version
if %ERRORLEVEL% EQU 0 (
    echo Slither installed successfully!
) else (
    echo Slither installation failed
    exit /b 1
)

REM Install Solidity compiler
echo Installing Solidity compiler...
pip install solc-select

REM Install and use a stable Solidity version
solc-select install 0.8.20
solc-select use 0.8.20

echo Slither environment setup complete!
echo.
echo Usage:
echo   slither contract.sol
echo   slither contract.sol --json output.json
