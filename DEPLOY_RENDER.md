# 🚀 Deploy no Render

## Pré-requisitos
- ✅ Código no GitHub: https://github.com/JuniorBrugnaro/pix-cn-pay.git
- ✅ Conta no Render: https://render.com
- ✅ Credenciais CN Pay (Public Key + Secret Key)

---

## Passos para Deploy

### 1️⃣ Conectar Repositório ao Render

1. Acesse https://render.com/dashboard
2. Clique em **"New +"** → **"Web Service"**
3. Selecione **"Connect Git Repository"**
4. Busque por **`pix-cn-pay`** e conecte

---

### 2️⃣ Configurar Web Service

Preencha os campos:

| Campo | Valor |
|-------|-------|
| **Name** | `pix-cnpay` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Instance Type** | Free (ou Starter se quiser performance) |

---

### 3️⃣ Adicionar Environment Variables

Clique em **"Environment"** e adicione:

```
CNPAY_PUBLIC_KEY=financeiro_moqjrint4j9xhzzt
CNPAY_SECRET_KEY=c3qfmxlk7iw147u7g5b47l2u7eghbd6vi3sgsb908afhrcvh2tqsksoxi7zyr75e
WEBHOOK_SECRET=seu_webhook_secret_aqui
PORT=10000
DEBUG=False
```

**Atenção:** Altere `WEBHOOK_SECRET` para um valor seguro!

---

### 4️⃣ Copiar a URL do Webhook

Após o deploy, você receberá uma URL do tipo:
```
https://seu-app-12345.onrender.com
```

Adicione a variável (edite e salve):
```
WEBHOOK_URL=https://seu-app-12345.onrender.com/webhook
```

---

### 5️⃣ Configurar Webhook na CN Pay

1. Acesse o **Dashboard CN Pay**: https://painel.appcnpay.com
2. Vá em **Integrações** → **Webhooks**
3. Clique em **Adicionar Webhook**
4. Preencha:
   - **URL**: `https://seu-app-12345.onrender.com/webhook`
   - **Token**: Mesmo valor de `WEBHOOK_SECRET`
   - **Eventos**: Marque `TRANSACTION_PAID`

---

### 6️⃣ Deploy!

Clique em **"Deploy"** e aguarde ≈ 5 minutos

A URL final será algo como:
```
https://pix-cnpay.onrender.com
```

---

## ✅ Verificar se está funcionando

```bash
# Health check
curl https://seu-app-12345.onrender.com/health

# Resposta esperada:
# {"status":"ok","timestamp":"2026-02-03T...","service":"checkout-pix-cnpay"}
```

---

## 🔐 Segurança - IMPORTANTE!

⚠️ **NÃO COMMITTAR** suas credenciais reais no repositório!

Se acidentalmente commitar:
```bash
git log --oneline --all
git revert <commit-hash>
git push
```

---

## 🐛 Troubleshooting

### Erro: "CNPAY_PUBLIC_KEY não encontrada"
- Verifique se adicionou as env vars em **Environment** no Render
- Clique em **"Redeploy"** após adicionar

### QR Code não aparece
- Verifique o console do navegador (F12)
- Confira se `CNPAY_PUBLIC_KEY` e `CNPAY_SECRET_KEY` estão corretos

### Webhook não funciona
- Certifique-se que `WEBHOOK_SECRET` é igual ao token na CN Pay
- Verifique os logs no Render: **Logs** → procure por "webhook"

---

## 📊 Monitorar em Produção

No dashboard do Render, você pode:
- Ver logs em tempo real
- Verificar uso de CPU/memória
- Fazer rollback de versões
- Configurar alerts

---

## 🔄 Fazer atualizações

Simplesmente faça `push` para o GitHub:

```bash
git add .
git commit -m "feat: descrição da mudança"
git push origin main
```

Render detectará automaticamente e fará **rebuild** em ~5 minutos.

---

**Status:** ✅ Pronto para production!
