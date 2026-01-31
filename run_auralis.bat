@echo off
echo ========================================
echo    Starting Auralis Application
echo ========================================
echo.

REM Start backend server
echo Starting backend server on port 8000...
start "Auralis Backend" cmd /k "cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend server
echo Starting frontend server on port 3000...
start "Auralis Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo    Auralis is starting!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to stop all servers...
pause >nul

REM Kill the servers
taskkill /FI "WindowTitle eq Auralis Backend*" /T /F >nul 2>&1
taskkill /FI "WindowTitle eq Auralis Frontend*" /T /F >nul 2>&1

echo.
echo Servers stopped.
