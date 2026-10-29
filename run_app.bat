@echo off
title Cynbit ArchitectAI
echo ========================================================
echo Launching Cynbit ArchitectAI Streamlit Application...
echo ========================================================
python -m streamlit run app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying direct script path...
    "%APPDATA%\Python\Python314\Scripts\streamlit.exe" run app.py
)
pause
