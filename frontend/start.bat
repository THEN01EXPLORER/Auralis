@echo off
echo Starting Auralis Frontend...
echo.
cd /d %~dp0
echo Installing dependencies if needed...
call npm install
echo.
echo Starting development server...
echo Frontend will open at http://localhost:3000
echo.
call npm start
pause

