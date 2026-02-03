# ============================================================
# Script PowerShell para iniciar PIX CNPAY com ngrok
# ============================================================
# 
# Uso:
#   powershell -ExecutionPolicy Bypass -File START_DEV.ps1
#
# ou clique 2x neste arquivo (se .ps1 estiver associado)
# ============================================================

# Cores
$host.UI.RawUI.BackgroundColor = "Black"
$host.UI.RawUI.ForegroundColor = "Green"
Clear-Host

Write-Host "============================================================"
Write-Host "   PIX CNPAY - Inicializando com ngrok"
Write-Host "============================================================"
Write-Host ""

# Definir diretório
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# ============================================================
# 1. Verificar ngrok
# ============================================================
Write-Host "[INFO] Verificando ngrok..." -ForegroundColor Cyan
try {
    ngrok --version | Out-Null
    Write-Host "[OK] ngrok encontrado" -ForegroundColor Green
} catch {
    Write-Host "[ERRO] ngrok nao encontrado!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Instale ngrok:" -ForegroundColor Yellow
    Write-Host "  1. Visite: https://ngrok.com/download"
    Write-Host "  2. Baixe para Windows"
    Write-Host "  3. Extraia ngrok.exe neste diretorio"
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""

# ============================================================
# 2. Verificar Virtual Environment
# ============================================================
Write-Host "[INFO] Verificando virtual environment..." -ForegroundColor Cyan
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "[OK] Virtual environment encontrado" -ForegroundColor Green
} else {
    Write-Host "[ERRO] Virtual environment nao encontrado!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Crie com:" -ForegroundColor Yellow
    Write-Host "  python -m venv .venv"
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""

# ============================================================
# 3. Ativar Virtual Environment
# ============================================================
Write-Host "[INFO] Ativando virtual environment..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1
Write-Host "[OK] Virtual environment ativado" -ForegroundColor Green
Write-Host ""

# ============================================================
# 4. Iniciar ngrok em background
# ============================================================
Write-Host "[INFO] Iniciando ngrok..." -ForegroundColor Cyan
$ngrokProcess = Start-Process -FilePath "ngrok" -ArgumentList "http 5000" -PassThru -NoNewWindow
Write-Host "[OK] ngrok iniciado (PID: $($ngrokProcess.Id))" -ForegroundColor Green
Write-Host ""

# Aguardar ngrok inicializar
Write-Host "[INFO] Aguardando ngrok inicializar..." -ForegroundColor Cyan
Start-Sleep -Seconds 3

# ============================================================
# 5. Pegar URL do ngrok
# ============================================================
Write-Host "[INFO] Obtendo URL do ngrok..." -ForegroundColor Cyan
try {
    $ngrokUrl = (Invoke-WebRequest -Uri "http://127.0.0.1:4040/api/tunnels" -ErrorAction SilentlyContinue).Content | 
        ConvertFrom-Json | 
        Select-Object -ExpandProperty tunnels | 
        Select-Object -First 1 -ExpandProperty public_url
    
    Write-Host "[OK] URL ngrok: $ngrokUrl" -ForegroundColor Green
} catch {
    Write-Host "[AVISO] Nao conseguiu obter URL ngrok automaticamente" -ForegroundColor Yellow
    Write-Host "Verifique em: http://127.0.0.1:4040" -ForegroundColor Yellow
}

Write-Host ""

# ============================================================
# 6. Iniciar Flask
# ============================================================
Write-Host "[INFO] Iniciando Flask..." -ForegroundColor Cyan
Start-Process -FilePath "cmd" -ArgumentList "/k python app.py" -WindowStyle Normal
Write-Host "[OK] Flask iniciado em nova janela" -ForegroundColor Green
Write-Host ""

# Aguardar Flask inicializar
Start-Sleep -Seconds 3

# ============================================================
# 7. Abrir Browser
# ============================================================
Write-Host "[INFO] Abrindo browser..." -ForegroundColor Cyan
Start-Process "http://localhost:5000"
Write-Host "[OK] Browser aberto" -ForegroundColor Green
Write-Host ""

# ============================================================
# 8. Mostrar Status
# ============================================================
Write-Host "============================================================"
Write-Host "   STATUS: Em Execucao!" -ForegroundColor Green
Write-Host "============================================================"
Write-Host ""
Write-Host "URLS DISPONIVEIS:" -ForegroundColor Yellow
Write-Host "  Local:         http://localhost:5000"
Write-Host "  ngrok:         $ngrokUrl"
Write-Host "  ngrok Dashboard: http://127.0.0.1:4040"
Write-Host ""
Write-Host "PROXIMAS ETAPAS:" -ForegroundColor Yellow
Write-Host "  1. Copie a URL do ngrok"
Write-Host "  2. Configure em CN Pay Dashboard > Integrações > Webhooks"
Write-Host "  3. URL do webhook: $ngrokUrl/webhook"
Write-Host ""
Write-Host "Para parar: Feche as janelas do Flask e ngrok" -ForegroundColor Cyan
Write-Host ""

# Manter script rodando
Read-Host "Pressione Enter para sair e encerrar ngrok"

# ============================================================
# 9. Limpar
# ============================================================
Write-Host ""
Write-Host "[INFO] Encerrando ngrok..." -ForegroundColor Cyan
Stop-Process -Id $ngrokProcess.Id -ErrorAction SilentlyContinue
Write-Host "[OK] ngrok encerrado" -ForegroundColor Green
Write-Host ""
Write-Host "Adeus!" -ForegroundColor Green
