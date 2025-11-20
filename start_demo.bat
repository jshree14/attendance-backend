@echo off
echo ========================================
echo Student Attendance System - Demo Setup
echo ========================================
echo.

echo Step 1: Starting the server...
echo.
start "Attendance Server" cmd /k "python run.py"

echo Waiting for server to start...
timeout /t 5 /nobreak > nul

echo.
echo Step 2: Creating demo data...
echo.
python demo_data.py

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo The server is running in a separate window.
echo.
echo Now open your browser and go to:
echo http://localhost:8000/docs
echo.
echo Login with:
echo   Email: admin@demo.com
echo   Password: admin123
echo.
echo Press any key to open the browser automatically...
pause > nul

start http://localhost:8000/docs

echo.
echo Browser opened! Follow the instructions in the browser.
echo.
echo To stop the server, close the "Attendance Server" window.
echo.
pause
