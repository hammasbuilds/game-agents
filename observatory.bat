@echo off
rem Starts the Observatory control panel on 127.0.0.1:8777 and nothing else.
rem No browser tab: Launchpad opens the page itself once the port answers.
cd /d "%~dp0"
title Game Agents - Observatory
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" -m observatory.server %*
) else (
  python -m observatory.server %*
)
if errorlevel 1 pause
