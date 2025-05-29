@echo off
REM run_all_win.bat - Script khoi dong backend va frontend cho BA_tutor tren Windows

REM Khoi dong backend (port 3001)
echo [Backend] Dang khoi dong FastAPI tai http://localhost:3001 ...
REM Chay tu thu muc goc, import backend.api_server:app
start cmd /k "uvicorn backend.api_server:app --reload --port 3001"

REM Khoi dong frontend (port 3000)
echo [Frontend] Dang khoi dong Vite React tai http://localhost:3000 ...
start cmd /k "cd frontend && npm install && npm run dev"

echo.
echo ---
echo Truy cap frontend tai: http://localhost:3000
echo Truy cap backend API docs tai: http://localhost:3001/docs
echo ---
echo.
echo De dung, hay dong cac cua so cmd da mo.
