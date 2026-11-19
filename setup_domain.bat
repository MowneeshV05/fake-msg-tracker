@echo off
:: Automatically elevate if not running as Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

set HOSTS_FILE=%WINDIR%\System32\drivers\etc\hosts

findstr /i "fraud-message-tracking-system" %HOSTS_FILE% >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] fraud-message-tracking-system is already mapped in your hosts file.
) else (
    echo. >> %HOSTS_FILE%
    echo 127.0.0.1 fraud-message-tracking-system >> %HOSTS_FILE%
    echo 127.0.0.1 fraudmessagetracking >> %HOSTS_FILE%
    echo [OK] Added fraud-message-tracking-system to %HOSTS_FILE%
)

echo.
echo ================================================================
echo Success! Domain mapping configured.
echo You can now access your app at:
echo http://fraud-message-tracking-system:8501
echo ================================================================
echo.
pause
