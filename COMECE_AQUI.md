# ✅ SCRIPTS PRONTOS - Teste Rápido!

**Status**: 🟢 Pronto para usar  
**Data**: 03/02/2026

---

## 🚀 3 Scripts Criados

### 1️⃣ START_DEV.bat ⭐ **RECOMENDADO**

**Duplo clique para iniciar TUDO automaticamente!**

```
✅ Ativa virtual environment
✅ Inicia ngrok (túnel para internet)
✅ Inicia Flask server
✅ Abre browser em http://localhost:5000
```

**Resultado**:
- 3 janelas abertas
- Tudo rodando
- URL pública aparece na janela ngrok
- Browser pronto para testar

---

### 2️⃣ START_LOCAL.bat

**Para testes simples sem webhooks remotos**

```
✅ Ativa virtual environment
✅ Inicia Flask server
✅ Sem ngrok
```

**Quando usar**: Testes locais rápidos

---

### 3️⃣ START_DEV.ps1

**Versão PowerShell com logs detalhados**

```powershell
powershell -ExecutionPolicy Bypass -File START_DEV.ps1
```

---

## 📋 Pré-Requisitos (Fazer uma vez)

### ✅ Python & Virtual Env

```bash
cd "c:\Users\Administrator\Desktop\PIX CNPAY"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### ✅ ngrok (Para START_DEV.bat)

1. Download: **https://ngrok.com/download**
2. Selecione: **Windows**
3. Extraia `ngrok.exe` no diretório do projeto
4. Pronto!

**Verificar**:
```bash
ngrok --version
```

---

## 🎯 Começar Agora (3 Passos)

### Passo 1: Baixar ngrok (2 min)

- Abra: https://ngrok.com/download
- Baixe Windows
- Extraia `ngrok.exe` em `c:\Users\Administrator\Desktop\PIX CNPAY\`

### Passo 2: Executar START_DEV.bat (30 seg)

- Abra Explorador de Arquivos
- Navegue até: `PIX CNPAY`
- **Duplo clique** em `START_DEV.bat`

### Passo 3: Testar (1 min)

- Browser abre em `http://localhost:5000`
- Copie URL do ngrok (da janela ngrok)
- Teste criar PIX via curl ou Postman

---

## 💻 Após Iniciar (O que você verá)

### Janela 1: ngrok
```
Forwarding  https://abc123.ngrok.io -> http://localhost:5000
Web Interface  http://127.0.0.1:4040
```

✅ Copie: `https://abc123.ngrok.io`

### Janela 2: Flask
```
Running on http://0.0.0.0:5000
```

✅ Servidor rodando

### Janela 3: Browser
```
http://localhost:5000 (já aberta)
```

✅ Pronto para usar!

---

## 🧪 Testar Agora (Via curl ou Postman)

### Criar PIX

```bash
curl -X POST http://localhost:5000/api/create-pix \
  -H "Content-Type: application/json" \
  -d '{"amount": 25.00}'
```

**Resposta esperada** (status 201):
```json
{
  "success": true,
  "transactionId": "...",
  "pix": {
    "qrCode": "00020126...",
    "base64": "iVBOR..."
  }
}
```

### Registrar Webhook em CN Pay (2 min)

1. Abra: https://painel.appcnpay.com/panel
2. Menu: **Integrações** → **Webhooks**
3. URL: `https://abc123.ngrok.io/webhook` (copie do ngrok)
4. Eventos: Todas as checkboxes
5. Salve

### Simular Webhook

```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event": "TRANSACTION_PAID",
    "token": "test",
    "client": {"id": "1", "name": "Teste", "email": "teste@ex.com"},
    "transaction": {
      "id": "txn123",
      "identifier": "PIX_...",
      "status": "PAID",
      "amount": 25.00,
      "paymentMethod": "PIX"
    }
  }'
```

**Você deve ver nos logs do Flask**:
```
[INFO] Webhook recebido: TRANSACTION_PAID
[INFO] Transaction ID: txn123
[INFO] Status: PAID
```

✅ **Webhook funcionando!**

---

## 📁 Arquivos Criados

```
PIX CNPAY/
├── START_DEV.bat         ← Duplo clique aqui!
├── START_LOCAL.bat       (alternativa sem ngrok)
├── START_DEV.ps1         (PowerShell avançado)
├── GUIA_NGROK.md         (documentação completa)
└── README_SCRIPTS.md     (comparação de scripts)
```

---

## 📖 Documentação

| Arquivo | Leia quando |
|---------|------------|
| README_SCRIPTS.md | Entender os 3 scripts |
| GUIA_NGROK.md | Troubleshooting ngrok |
| PRÓXIMOS_PASSOS.md | Deploy em produção |

---

## ⚠️ Erros Comuns

### "ngrok não encontrado"

```bash
# Solução: Download e extrair ngrok.exe
# https://ngrok.com/download
```

### "Porta 5000 em uso"

```bash
# Mude em .env:
PORT=5001

# E rode ngrok em 5001:
ngrok http 5001
```

### "Browser não abre"

- Abra manualmente: `http://localhost:5000`

---

## ✅ Checklist

- [ ] Python 3.8+ instalado
- [ ] Virtual environment criado (`.venv`)
- [ ] ngrok.exe no diretório
- [ ] ngrok --version funciona
- [ ] Duplo clique em START_DEV.bat
- [ ] 3 janelas abertas
- [ ] Browser em localhost:5000
- [ ] URL ngrok copiada
- [ ] Webhook registrado em CN Pay
- [ ] Teste de PIX funcionando

---

## 🎉 Próximo Passo

### Agora:
```
Duplo clique em START_DEV.bat
```

### Depois (30 min):
- Testar criação de PIX
- Registrar webhook em CN Pay
- Testar pagamento

### Finalmente (quando pronto):
- Deploy no Render
- [Ver PRÓXIMOS_PASSOS.md](PRÓXIMOS_PASSOS.md)

---

**Versão**: 1.0  
**Status**: ✅ Pronto para usar  
**Data**: 03/02/2026

🚀 **Comece agora! Duplo clique em START_DEV.bat**
