@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0start-local.ps1"
if errorlevel 1 (
  pause
  exit /b 1
)
start "" "http://localhost:5173"
