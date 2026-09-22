@echo off
REM ====================================================================
REM  Windows Endpoint Setup Script
REM  Author: Dil Mahmud Khan
REM  Prepares the lab workspace on the Windows target VM
REM ====================================================================

echo [*] Initializing Lab Environment on Windows...
if not exist "C:\LabAttacks" (
    mkdir "C:\LabAttacks"
    echo [✓] Created working directory C:\LabAttacks
) else (
    echo [*] Directory C:\LabAttacks already exists.
)

echo [*] Testing PowerShell execution policy...
powershell -Command "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force"
echo [✓] Execution policy set for current session.

echo [*] Setup complete. Ready to install LimaCharlie sensor and run attack scenarios.
pause
