$ErrorActionPreference = 'Stop'
$projectDirectory = $PSScriptRoot
$nodeExecutable = (Get-Command node.exe -ErrorAction Stop).Source
$logDirectory = Join-Path $projectDirectory 'logs'
New-Item -ItemType Directory -Force -Path $logDirectory | Out-Null

# Use the same configuration as the backend before starting any server.
& $nodeExecutable (Join-Path $projectDirectory 'backend-js/tests/check-db.js')
if ($LASTEXITCODE -ne 0) { throw 'Database tidak tersedia. Jalankan MySQL melalui Start All di Laragon.' }

function Start-LocalServer($Port, $Directory, $Arguments, $Name) {
    $listener = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if (-not $listener) {
        Start-Process -FilePath $nodeExecutable -ArgumentList $Arguments `
            -WorkingDirectory (Join-Path $projectDirectory $Directory) -WindowStyle Hidden `
            -RedirectStandardOutput (Join-Path $logDirectory "$Name.log") `
            -RedirectStandardError (Join-Path $logDirectory "$Name-error.log") | Out-Null
    }
}

Start-LocalServer 3000 'backend-js' 'index.js' 'backend'
Start-LocalServer 5173 'frontend' 'node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5173 --strictPort' 'frontend'

$ready = $false
for ($attempt = 0; $attempt -lt 20; $attempt++) {
    try {
        $health = Invoke-RestMethod 'http://127.0.0.1:3000/api/health' -TimeoutSec 2
        $page = Invoke-WebRequest 'http://127.0.0.1:5173' -UseBasicParsing -TimeoutSec 2
        if ($health.database -eq 'connected' -and $page.Content -match '/src/main.js') {
            $ready = $true
            break
        }
    } catch { Start-Sleep -Milliseconds 500 }
}
if (-not $ready) { throw "Server belum siap atau port dipakai aplikasi lain. Periksa $logDirectory" }
Write-Host 'Sustainova aktif: http://localhost:5173'
Write-Host 'Database: sustainova | Backend: http://localhost:3000/api/health'
