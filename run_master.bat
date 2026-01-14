@echo off
REM Open the master dashboard without regenerating it
REM Just displays the existing outputs/index.html file

echo Opening master dashboard...

if not exist "outputs\index.html" (
    echo ERROR: Master dashboard not found at outputs\index.html
    echo Run deploy_master.bat first to generate it.
    pause
    exit /b 1
)

start outputs\index.html

echo Master dashboard opened in browser.
