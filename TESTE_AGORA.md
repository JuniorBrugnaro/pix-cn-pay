# 🎯 PRONTO PARA TESTAR - Comandos Rápidos

**Data**: 03/02/2026  
**Status**: ✅ Tudo configurado na porta 5000

---

## 🌐 URLs Atualizadas

```
Local:       http://localhost:5000
ngrok:       https://83e5cd1fa34a.ngrok-free.app  (sua URL)
ngrok UI:    http://127.0.0.1:4040
```

---

## 🚀 Passo 1: Iniciar ngrok (Porta 5000)

```bash
cd "c:\Users\Administrator\Desktop\PIX CNPAY"
ngrok http 5000
```

**Você verá**:
```
Forwarding  https://83e5cd1fa34a.ngrok-free.app -> http://localhost:5000
```

✅ Copie a URL ngrok (muda cada vez que reinicia)

---

## 🚀 Passo 2: Iniciar Flask (Em outro Terminal)

```bash
cd "c:\Users\Administrator\Desktop\PIX CNPAY"
.venv\Scripts\activate
python app.py
```

**Você verá**:
```
Running on http://0.0.0.0:5000
```

---

## ✅ Passo 3: Testar Endpoints

### Teste 1: Health Check (Simples)

```bash
curl http://localhost:5000/health
```

**Resposta esperada**:
```json
{
  "status": "ok",
  "timestamp": "2026-02-03T...",
  "service": "checkout-pix-cnpay"
}
```

### Teste 2: Criar PIX

```bash
curl -X POST http://localhost:5000/api/create-pix \
  -H "Content-Type: application/json" \
  -d '{"amount": 25.00}'
```

**Resposta esperada (status 201)**:
```json
{
  "success": true,
  "transactionId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "identifier": "PIX_1707254...",
  "status": "PENDING",
  "pix": {
    "qrCode": "00020126...",
    "base64": "iVBOR..."
  }
}
```

✅ **Copie o `transactionId`**

### Teste 3: Verificar Pagamento

```bash
curl "http://localhost:5000/api/check-payment/TRANSACTION_ID_AQUI"
```

**Substitua `TRANSACTION_ID_AQUI`** pelo ID que você copiou

---

## 🔔 Passo 4: Testar Webhook

### Teste Manual (Sem parar Flask/ngrok)

Abra **outro terminal**:

```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event": "TRANSACTION_PAID",
    "token": "test-token",
    "client": {
      "id": "123",
      "name": "Teste Silva",
      "email": "teste@example.com"
    },
    "transaction": {
      "id": "txn-123",
      "identifier": "PIX_1707254...",
      "status": "PAID",
      "amount": 25.00,
      "paymentMethod": "PIX",
      "pixInformation": {
        "qrCode": "00020126...",
        "endToEndId": "E123456..."
      }
    }
  }'
```

**Nos logs do Flask você verá**:
```
[INFO] Webhook recebido: TRANSACTION_PAID
[INFO] Transaction ID: txn-123
[INFO] Status: PAID
[INFO] Valor: R$ 25.00
[INFO] Cliente: Teste Silva - teste@example.com
```

✅ **Webhook funcionando!**

---

## 📊 Via ngrok Dashboard

Para inspecionar requisições em tempo real:

1. Abra: **http://127.0.0.1:4040**
2. Veja todas as requisições
3. Clique em qualquer uma para detalhes completos
4. Opção "Replay" para repetir requisição

---

## 🔗 Registrar em CN Pay

### URL do Webhook

Use a URL ngrok (aquela que começa com `https://`):

```
https://83e5cd1fa34a.ngrok-free.app/webhook
```

### Steps no Dashboard CN Pay

1. Abra: https://painel.appcnpay.com/panel
2. Menu: **Integrações** → **Webhooks**
3. Clique: **Adicionar Webhook**
4. URL: Cole a URL ngrok + `/webhook`
5. Eventos (marque todos):
   - [x] TRANSACTION_PAID
   - [x] TRANSACTION_CREATED
   - [x] TRANSACTION_CANCELED
   - [x] TRANSACTION_REFUNDED
6. Salve

✅ Pronto! CN Pay enviará webhooks para seu localhost via ngrok

---

## 🧪 Teste Completo

```bash
# Terminal 1: ngrok
ngrok http 5000

# Terminal 2: Flask
python app.py

# Terminal 3: Teste (Health Check)
curl http://localhost:5000/health

# Terminal 3: Teste (Criar PIX)
curl -X POST http://localhost:5000/api/create-pix \
  -H "Content-Type: application/json" \
  -d '{"amount": 0.01}'

# Terminal 3: Teste (Webhook)
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{...}'
```

---

## 📝 Dicas Importantes

### URL ngrok Muda a Cada Reinicialização

- Primeira vez: `https://abc123.ngrok-free.app`
- Próxima vez: `https://xyz789.ngrok-free.app`

**Solução**: Sempre atualize URL em CN Pay quando reiniciar ngrok

### Para URL Fixa (Opcional)

1. Crie conta em: https://ngrok.com/signup
2. Copie `authtoken`
3. Rode: `ngrok authtoken SEU_TOKEN`
4. Agora URLs ngrok são fixas!

### Logs em Tempo Real

- **Flask logs**: No terminal que rodou `python app.py`
- **ngrok logs**: No terminal que rodou `ngrok http 5000`
- **Web UI**: http://127.0.0.1:4040

---

## ✅ Checklist

- [x] Porta configurada em .env (5000)
- [x] ngrok instalado e funcionando
- [x] Flask testado localmente
- [ ] ngrok rodando (porta 5000)
- [ ] Flask rodando (app.py)
- [ ] Health check funcionando
- [ ] Criar PIX funcionando
- [ ] Webhook registrado em CN Pay
- [ ] Webhook testado manualmente

---

## 🎯 Próximos Passos

### Agora (5 min):
1. Rode: `ngrok http 5000`
2. Rode: `python app.py`
3. Teste os comandos acima

### Depois (10 min):
1. Registre webhook em CN Pay
2. Teste fluxo completo

### Finalmente:
1. Deploy no Render
2. Veja: [PRÓXIMOS_PASSOS.md](PRÓXIMOS_PASSOS.md)

---

**Versão**: 1.0  
**Data**: 03/02/2026  
**Status**: ✅ Pronto para testes

🚀 **Comece a testar agora!**
