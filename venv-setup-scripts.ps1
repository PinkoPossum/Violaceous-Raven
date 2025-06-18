# =============================
# Auto-downgrade & Setup Python 3.12 Environment
# =============================

Write-Host "Extracting current environment requirements..."
if (Test-Path ".venv\Scripts\python.exe") {
    .\.venv\Scripts\python.exe -m pip freeze > requirements.txt
    Write-Host "✅ requirements.txt created from existing .venv."
} else {
    Write-Host "⚠️ Existing .venv not found or invalid. Skipping freeze step."
}

# Check if Python 3.12 is installed
Write-Host "🔍 Checking for Python 3.12..."
$py312 = Get-Command "py -3.12" -ErrorAction SilentlyContinue

if (-not $py312) {
    Write-Host "📥 Python 3.12 not found. Downloading installer..."
    $installerUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    $installerPath = "$env:TEMP\python312_installer.exe"
    Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath

    Write-Host "🚀 Running installer (you may be prompted)..."
    Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0" -Wait
} else {
    Write-Host "✅ Python 3.12 is already installed."
}

# Backup old venv
if (Test-Path ".venv") {
    $timestamp = Get-Date -Format "yyyyMMddHHmmss"
    Rename-Item ".venv" ".venv_backup_$timestamp"
    Write-Host "🧼 Backed up old .venv as '.venv_backup_$timestamp'"
}

# Create new venv
Write-Host "🐍 Creating new .venv with Python 3.12..."
py -3.12 -m venv .venv

# Activate and install packages
Write-Host "📦 Activating new environment..."
. .\.venv\Scripts\Activate.ps1

if (Test-Path "requirements.txt") {
    Write-Host "📥 Installing dependencies from requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
} else {
    Write-Host "⚠️ No requirements.txt found to install packages."
}

Write-Host "`n🎉 All done!"
Write-Host "🛠️ Be sure to update your IDE to use the new .venv Python interpreter."
