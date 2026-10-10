@echo off
REM In Command Prompt: run, then run import issues.csv, then run report.
REM A single CSV still works: run issues.csv
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" %*
exit /b %ERRORLEVEL%
