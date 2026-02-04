@echo off
REM ============================================================
REM Script para iniciar PIX CNPAY com ngrok em localhost
REM ============================================================
REM
REM Este script:
REM 1. Verifica pré-requisitos (ngrok, venv)
REM 2. Inicia ngrok na porta 5000
REM 3. Inicia Flask (carrega .env automaticamente)
REM 4. Abre browser em localhost:5000
REM
REM ============================================================

setlocal enabledelayedexpansion

REM Cores e estilos
color 0A
title PIX CNPAY - Dev Server com ngrok

REM Definir diretório
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo.
echo ============================================================
echo   PIX CNPAY - Inicializando ambiente de desenvolvimento
echo ============================================================
echo.

REM ============================================================
REM 1. VERIFICAR PRÉ-REQUISITOS
REM ============================================================

REM Verificar ngrok
ngrok --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERRO] ngrok nao encontrado!
    echo.
    echo Para instalar:
    echo   1. Visite: https://ngrok.com/download
    echo   2. Baixe para Windows
    echo   3. Extraia ngrok.exe neste diretorio: %SCRIPT_DIR%
    echo   4. Execute novamente este script
    echo.
    pause
    exit /b 1
)
echo [OK] ngrok encontrado
color 0A

REM Verificar virtual env
if not exist ".venv\Scripts\activate.bat" (
    color 0C
    echo [ERRO] Virtual environment nao encontrado!
    echo.
    echo Para criar:
    echo   python -m venv .venv
    echo   .venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)
echo [OK] Virtual environment encontrado
echo.

REM Verificar .env
if not exist ".env" (
    color 0C
    echo [ERRO] Arquivo .env nao encontrado!
    echo.
    echo Crie um .env com suas credenciais CN Pay
    echo.
    pause
    exit /b 1
)
echo [OK] Arquivo .env encontrado
echo.

REM ============================================================
REM 2. ATIVAR VENV
REM ============================================================
call .venv\Scripts\activate.bat

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERRO] Python nao encontrado no venv!
    pause
    exit /b 1
)

echo [OK] Python ativado
echo.

REM ============================================================
REM 3. INICIAR NGROK
REM ============================================================
color 0E
echo [INFO] Iniciando ngrok na porta 5000...
echo.
start "ngrok - PIX CNPAY" cmd /k "ngrok http 5000"

REM Aguardar ngrok inicializar
echo [INFO] Aguardando ngrok inicializar...
timeout /t 4 /nobreak

echo.

REM ============================================================
REM 4. INICIAR FLASK
REM ============================================================
color 0A
echo [INFO] Iniciando Flask Server...
echo.
start "Flask - PIX CNPAY" cmd /k "python app.py"

REM Aguardar Flask inicializar
echo [INFO] Aguardando Flask inicializar...
timeout /t 3 /nobreak

REM ============================================================
REM 5. ABRIR BROWSER
REM ============================================================
echo [INFO] Abrindo browser...
start http://localhost:5000

echo.
echo ============================================================
echo   STATUS: EXECUTANDO!
echo ============================================================
echo.
echo URLS DISPONIVEIS:
echo   Local:         http://localhost:5000
echo   ngrok:         Verifique na janela do ngrok (https://...)
echo   ngrok Dashboard: http://127.0.0.1:4040
echo.
echo PROXIMOS PASSOS:
echo   1. Copie a URL do ngrok (janela ngrok)
echo   2. Configure em CN Pay Dashboard:
echo      Integraciones ^> Webhooks
echo   3. URL do webhook: https://xxxxx.ngrok-free.app/webhook
echo.
echo PARA PARAR:
echo   Feche as janelas do ngrok e Flask
echo.
pause

echo.
echo ============================================================
echo   STATUS: Executando!
echo ============================================================
echo.
echo URLS DISPONIVEIS:
echo   Local:  http://localhost:5000
echo   ngrok:  Verifique na janela do ngrok (URL dinamica)
echo.
echo DICAS:
echo   1. Copie a URL do ngrok (https://xxxxx.ngrok.io)
echo   2. Configure em CN Pay Dashboard > Integracoes > Webhooks
echo   3. URL do webhook: https://xxxxx.ngrok.io/webhook
echo.
echo Para parar: Feche as janelas do Flask e ngrok
echo.

pause
