@echo off
REM ============================================================
REM Script simples para iniciar PIX CNPAY em localhost
REM (Sem ngrok - apenas para testes locais)
REM ============================================================

setlocal enabledelayedexpansion

color 0A
title PIX CNPAY - Dev Server

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo.
echo ============================================================
echo   PIX CNPAY - Inicializando (Localhost)
echo ============================================================
echo.

REM Verificar virtual env
if not exist ".venv\Scripts\activate.bat" (
    echo [ERRO] Virtual environment nao encontrado!
    echo.
    echo Crie com o comando:
    echo   python -m venv .venv
    echo.
    pause
    exit /b 1
)

REM Ativar venv
call .venv\Scripts\activate.bat

echo [OK] Virtual environment ativado
echo.
echo [INFO] Iniciando servidor Flask...
echo.
echo ============================================================
echo   Acesse: http://localhost:5000
echo ============================================================
echo.
echo Para parar: Pressione Ctrl+C
echo.

python app.py
