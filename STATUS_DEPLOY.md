# ✅ Setup Automático - Pronto para Deploy

## 🚀 O que foi feito

### ✨ Detecção Automática de Ambiente
- ✅ WEBHOOK_URL detecta automaticamente se está em Render
- ✅ Hardcoded para `https://pix-cnpay.onrender.com/webhook`
- ✅ Em local (ngrok), continua funcionando normalmente

### 📦 Configurações Aplicadas

**`.env`** - Atualizado com:
```
WEBHOOK_URL=https://pix-cnpay.onrender.com/webhook
PORT=5000
DEBUG=False
```

**`app.py`** - Melhorias:
- Detecção automática de ambiente (Render vs Local)
- Logs informativos na inicialização
- Inferência inteligente de WEBHOOK_URL

**`Procfile`** - Otimizado para Render:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 3 --timeout 120
```

**`run.sh`** - Script de inicialização production-ready

---

## 🎯 Como Fazer Deploy Agora

### 1. No Render Dashboard
```
1. Acesse https://render.com/dashboard
2. Clique em "New Web Service"
3. Conecte: https://github.com/JuniorBrugnaro/pix-cn-pay
4. Configure:
   - Name: pix-cnpay
   - Region: São Paulo (sa)
   - Runtime: Python 3
5. Build & Deploy!
```

### 2. Environment Variables (Render)
```
CNPAY_PUBLIC_KEY=financeiro_moqjrint4j9xhzzt
CNPAY_SECRET_KEY=c3qfmxlk7iw147u7g5b47l2u7eghbd6vi3sgsb908afhrcvh2tqsksoxi7zyr75e
WEBHOOK_SECRET=seu-webhook-secret
PORT=10000
DEBUG=False
```

### 3. Na CN Pay Dashboard
```
URL: https://pix-cnpay.onrender.com/webhook
Token: Mesmo valor de WEBHOOK_SECRET
Evento: TRANSACTION_PAID
```

---

## 📊 Status do Deploy

| Componente | Status |
|---|---|
| GitHub | ✅ Sincronizado |
| .env | ✅ Configurado |
| app.py | ✅ Autodetecção ativada |
| Procfile | ✅ Otimizado |
| Documentação | ✅ DEPLOY_RENDER.md pronto |

---

## 🔄 Workflow de Atualizações

Após deploy, qualquer mudança no código:
```bash
git add .
git commit -m "feat: descrição"
git push origin main
```

**Render detectará automaticamente e fará redeploy em ~5 minutos**

---

## ✅ Checklist Final Antes do Deploy

- [ ] Acessar https://github.com/JuniorBrugnaro/pix-cn-pay
- [ ] Verificar se main branch está atualizado
- [ ] Criar novo Web Service no Render
- [ ] Adicionar as 5 env vars
- [ ] Clicar "Deploy"
- [ ] Aguardar ~5-10 minutos
- [ ] Testar em https://pix-cnpay.onrender.com
- [ ] Registrar webhook na CN Pay
- [ ] Fazer teste de pagamento

---

**Status:** 🟢 PRONTO PARA PRODUÇÃO!
