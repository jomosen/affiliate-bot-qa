# Windows PowerShell setup script for Affiliate Bot QA
# Creates .venv, installs dependencies, and installs Playwright browsers

param(
    [string]$PythonPath = "python"
)

Write-Host "========== Affiliate Bot QA Setup ==========" -ForegroundColor Cyan

# Check Python version
try {
    $versionOutput = & $PythonPath --version
    Write-Host "Python version: $versionOutput" -ForegroundColor Green
} catch {
    Write-Host "Python not found. Please install Python 3.10+ and rerun." -ForegroundColor Red
    exit 1
}

# Create virtual environment if missing
$venvDir = ".venv"
if (Test-Path $venvDir) {
    Write-Host ".venv already exists" -ForegroundColor Yellow
} else {
    Write-Host "Creating virtual environment (.venv)..." -ForegroundColor Cyan
    & $PythonPath -m venv $venvDir
}

# Paths inside venv
$venvPython = Join-Path $venvDir "Scripts/python.exe"
$venvPip = Join-Path $venvDir "Scripts/pip.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "Virtual environment python not found. Setup failed." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "Installing Python dependencies into .venv..." -ForegroundColor Cyan
& $venvPip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { Write-Host "pip install failed" -ForegroundColor Red; exit 1 }

# Install Playwright browsers
Write-Host "Installing Playwright browsers (chromium)..." -ForegroundColor Cyan
& $venvPython -m playwright install chromium
if ($LASTEXITCODE -ne 0) { Write-Host "playwright install failed" -ForegroundColor Red; exit 1 }

# Copy .env.example to .env if it doesn't exist
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✓ Created .env from .env.example" -ForegroundColor Green
        Write-Host "⚠ Remember to edit .env with your configuration" -ForegroundColor Yellow
    }
} else {
    Write-Host "✓ .env already exists" -ForegroundColor Green
}

# Done
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "Activate the venv with:" -ForegroundColor Cyan
Write-Host ".venv\\Scripts\\Activate.ps1" -ForegroundColor Yellow
Write-Host "Then run commands, e.g.:" -ForegroundColor Cyan
Write-Host "python -m src.main --dry-run" -ForegroundColor Yellow
