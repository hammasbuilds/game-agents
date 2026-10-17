@echo off
rem Serves the public dashboard (docs/) on 127.0.0.1:8779.
rem The same page that is published to GitHub Pages, read from this checkout.
cd /d "%~dp0"
title Game Agents - dashboard
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" -m http.server 8779 --bind 127.0.0.1 --directory docs
) else (
  python -m http.server 8779 --bind 127.0.0.1 --directory docs
)
if errorlevel 1 pause
