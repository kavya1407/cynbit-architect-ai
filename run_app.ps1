Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Launching Cynbit ArchitectAI Streamlit Application..." -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

try {
    python -m streamlit run app.py
} catch {
    Write-Host "Trying direct script path..." -ForegroundColor Yellow
    & "$env:APPDATA\Python\Python314\Scripts\streamlit.exe" run app.py
}
