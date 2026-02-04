#!/bin/bash
# Script para executar a aplicação no Render

# Definir variáveis de produção
export FLASK_APP=app.py
export FLASK_ENV=production
export DEBUG=False

# Se PORT não estiver definido, usar 10000 (default do Render)
export PORT=${PORT:-10000}

# Executar com gunicorn
gunicorn \
  --workers=3 \
  --worker-class=sync \
  --bind=0.0.0.0:${PORT} \
  --timeout=120 \
  --access-logfile - \
  --error-logfile - \
  app:app
