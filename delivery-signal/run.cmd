@echo off
REM One command for cmd. Windows already includes PowerShell. This does not install it.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" %*
exit /b %ERRORLEVEL%
