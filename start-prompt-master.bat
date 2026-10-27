@echo off
cd /d "%~dp0"
start "Prompt Master Server" /min node server.js
timeout /t 2 /nobreak >nul
start "Prompt Master" http://127.0.0.1:8765/index.html
