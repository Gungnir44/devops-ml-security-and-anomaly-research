@echo off
REM Automatic Weekly Artifact Download
REM Run this script weekly to download artifacts from scheduled workflows

cd /d "C:\Users\joshu\Desktop\DevOps Project\scripts"

echo ========================================
echo Weekly Artifact Download
echo ========================================
echo Started: %date% %time%
echo.

REM Download scheduled artifacts
python download_scheduled_artifacts.py

echo.
echo ========================================
echo Download Complete
echo ========================================
echo Finished: %date% %time%
echo.

REM Optional: Keep window open to see results
pause
