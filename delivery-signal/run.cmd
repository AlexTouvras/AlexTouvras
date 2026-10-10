@echo off
REM One command in your own Command Prompt: run issues.csv
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" %*
exit /b %ERRORLEVEL%
