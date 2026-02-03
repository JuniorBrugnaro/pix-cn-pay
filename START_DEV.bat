@echo off
REM ============================================================
REM Script para iniciar PIX CNPAY com ngrok em localhost
REM ============================================================
REM
REM Este script:
REM 1. Ativa o virtual environment
REM 2. Inicia o servidor Flask
REM 3. Inicia ngrok para tunelar localhost para internet
REM 4. Abre o browser em localhost:5000
REM
REM ============================================================

setlocal enabledelayedexpansion

REM Cores e estilos
color 0A
title PIX CNPAY - Desenvolvimento Local com ngrok

REM Definir diretório
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo.
echo ============================================================
echo   PIX CNPAY - Inicializando...
echo ============================================================
echo.

REM Verificar se ngrok está instalado
ngrok --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] ngrok nao encontrado!
    echo.
    echo Instale ngrok:
    echo   1. Visite: https://ngrok.com/download
    echo   2. Baixe para Windows
    echo   3. Extraia ngrok.exe para este diretorio
    echo   4. Execute novamente este script
    echo.
    pause
    exit /b 1
)

echo [OK] ngrok encontrado
echo.

REM Verificar se virtual env existe
if not exist ".venv\Scripts\activate.bat" (
    echo [ERRO] Virtual environment nao encontrado!
    echo Crie com: python -m venv .venv
    pause
    exit /b 1
)

echo [OK] Virtual environment encontrado
echo.

REM Ativar venv e verificar
call .venv\Scripts\activate.bat
python --version

REM Iniciar ngrok em janela separada
echo [INFO] Iniciando ngrok em outra janela...
start "ngrok - PIX CNPAY" cmd /k ngrok http 5000

REM Aguardar ngrok inicializar (5 segundos)
timeout /t 5 /nobreak

REM Iniciar Flask em janela separada
echo [INFO] Iniciando Flask em outra janela...
start "Flask - PIX CNPAY" cmd /k python app.py

REM Aguardar Flask inicializar (3 segundos)
timeout /t 3 /nobreak

REM Abrir browser
echo [INFO] Abrindo browser em localhost:5000...
start http://localhost:5000

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
