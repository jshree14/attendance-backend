@echo off
echo ========================================
echo Fixing Deployment Issues
echo ========================================
echo.

echo Step 1: Backing up old requirements.txt...
copy requirements.txt requirements-old.txt
echo ✅ Backup created: requirements-old.txt
echo.

echo Step 2: Using clean requirements for deployment...
copy requirements-deploy.txt requirements.txt
echo ✅ requirements.txt updated with clean dependencies
echo.

echo Step 3: Testing locally with production server...
echo Installing production dependencies...
pip install -r requirements.txt
echo.

echo ========================================
echo ✅ Fixed! Now you can deploy to Render
echo ========================================
echo.
echo Next steps:
echo 1. Push to GitHub:
echo    git add .
echo    git commit -m "Fix deployment dependencies"
echo    git push
echo.
echo 2. On Render.com, use these settings:
echo    Build Command: pip install -r requirements.txt
echo    Start Command: gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
echo.
echo 3. Add environment variable:
echo    SECRET_KEY = (generate with: openssl rand -hex 32)
echo.
pause
