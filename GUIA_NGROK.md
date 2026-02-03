# 🌐 Guia: Configurar ngrok para Testes com Webhooks

**Data**: 03/02/2026  
**Objetivo**: Testar webhooks em localhost com URL pública

---

## 📋 O que é ngrok?

ngrok cria um **túnel seguro** entre sua máquina local (localhost) e a internet.

```
Seu PC (localhost:5000) 
    ↓
ngrok (cria URL pública)
    ↓
CN Pay consegue acessar
    ↓
Webhooks funcionam em localhost!
```

---

## ⚙️ Passo 1: Instalar ngrok

### Opção A: Download Direto (Recomendado)

1. Acesse: **https://ngrok.com/download**
2. Selecione **Windows**
3. Baixe o arquivo `.zip`
4. Extraia em: `c:\Users\Administrator\Desktop\PIX CNPAY\`

**Resultado**: Você terá `ngrok.exe` no diretório do projeto

### Opção B: Usar Chocolatey (se tiver)

```bash
choco install ngrok
```

### Opção C: Usar npm (se tiver Node.js)

```bash
npm install -g ngrok
```

---

## ✅ Passo 2: Verificar Instalação

Abra PowerShell/CMD e digite:

```bash
ngrok --version
```

**Deve retornar**: `ngrok version 3.x.x`

---

## 🚀 Passo 3: Usar o Script Automático

### Método A: START_DEV.bat (Recomendado)

Abra o Explorador de Arquivos, navegue até a pasta do projeto e **clique 2x em `START_DEV.bat`**

**Isso vai**:
1. ✅ Ativar virtual environment
2. ✅ Iniciar ngrok em janela separada
3. ✅ Iniciar Flask em janela separada
4. ✅ Abrir browser automaticamente

**Você verá 3 janelas**:
- Janela 1: Flask rodando em `http://localhost:5000`
- Janela 2: ngrok com URL pública (ex: `https://abc123.ngrok.io`)
- Janela 3: Browser aberto

### Método B: Manual (Para Entender o Processo)

#### Terminal 1: Iniciar Flask
```bash
cd "c:\Users\Administrator\Desktop\PIX CNPAY"
.venv\Scripts\activate
python app.py
```

#### Terminal 2: Iniciar ngrok
```bash
cd "c:\Users\Administrator\Desktop\PIX CNPAY"
ngrok http 5000
```

**Você verá na saída do ngrok**:
```
Session started
Forwarding                    https://abc123.ngrok.io -> http://localhost:5000
```

Copie a URL: `https://abc123.ngrok.io`

---

## 📌 Registrar Webhook em CN Pay

1. Abra: **https://painel.appcnpay.com/panel**
2. Menu: **Integrações** → **Webhooks**
3. Clique em **Adicionar Webhook**
4. Cola a URL do ngrok: `https://abc123.ngrok.io/webhook`
5. Eventos:
   - [x] TRANSACTION_PAID
   - [x] TRANSACTION_CREATED
   - [x] TRANSACTION_CANCELED
   - [x] TRANSACTION_REFUNDED
6. Salve

---

## 🧪 Testar Webhook

### Teste 1: Criar PIX

```bash
curl -X POST https://abc123.ngrok.io/api/create-pix \
  -H "Content-Type: application/json" \
  -d '{"amount": 0.01}'
```

Copie o `transactionId` da resposta.

### Teste 2: Simular Webhook

```bash
curl -X POST https://abc123.ngrok.io/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event": "TRANSACTION_PAID",
    "token": "test",
    "client": {
      "id": "123",
      "name": "Teste",
      "email": "teste@example.com"
    },
    "transaction": {
      "id": "txn123",
      "identifier": "PIX_...",
      "status": "PAID",
      "amount": 0.01,
      "paymentMethod": "PIX"
    }
  }'
```

### Teste 3: Verificar no Terminal do Flask

Você deve ver nos logs do Flask:

```
[INFO] Webhook recebido: TRANSACTION_PAID
[INFO] Transaction ID: txn123
[INFO] Status: PAID
[INFO] Valor: R$ 0.01
```

✅ **Webhook funcionando!**

---

## 📊 URLs Disponíveis Durante Teste

| Local | URL |
|-------|-----|
| Browser | `http://localhost:5000` |
| API Local | `http://localhost:5000/api/create-pix` |
| ngrok Dashboard | `http://127.0.0.1:4040` |
| API via ngrok | `https://abc123.ngrok.io/api/create-pix` |
| Webhook via ngrok | `https://abc123.ngrok.io/webhook` |

---

## 🔍 ngrok Dashboard

Enquanto ngrok está rodando, acesse:

```
http://127.0.0.1:4040
```

Lá você pode:
- ✅ Ver todas as requisições
- ✅ Inspecionar headers e body
- ✅ Reproduzir requisições
- ✅ Testar webhooks manualmente

---

## ⚠️ Cuidados Importantes

### Porta Dinâmica
A URL do ngrok muda **toda vez** que você reinicia:
- Primeira execução: `https://abc123.ngrok.io`
- Próxima execução: `https://xyz789.ngrok.io`

**Solução**: Sempre atualize a URL em CN Pay quando reiniciar ngrok, OU use ngrok com conta (URL fixa).

### ngrok com Conta (URL Fixa) - Opcional

1. Crie conta em: https://ngrok.com/signup
2. Copie seu **authtoken** do dashboard
3. Rode: `ngrok authtoken SEU_TOKEN`
4. Agora suas URLs ngrok são fixas!

---

## 🐛 Troubleshooting

### Erro: "ngrok.exe não encontrado"

```
[ERRO] ngrok nao encontrado!
```

**Solução**:
1. Download ngrok: https://ngrok.com/download
2. Extraia em: `c:\Users\Administrator\Desktop\PIX CNPAY\`
3. Verifique se `ngrok.exe` está no mesmo diretório do `START_DEV.bat`

### Erro: "Virtual environment não encontrado"

```
[ERRO] Virtual environment nao encontrado!
```

**Solução**:
```bash
cd "c:\Users\Administrator\Desktop\PIX CNPAY"
python -m venv .venv
```

### ngrok conectado mas webhook não recebe

1. Verifique URL em CN Pay (copie corretamente)
2. Teste manualmente com curl
3. Veja logs no ngrok Dashboard: `http://127.0.0.1:4040`

### Porta 5000 já em uso

```
Address already in use
```

**Solução**: Mude porta em `.env`:
```
PORT=5001
```

E rode ngrok: `ngrok http 5001`

---

## 📝 Resumo Rápido

```bash
# 1. Instalar ngrok (uma vez)
# Baixe de https://ngrok.com/download

# 2. Colocar ngrok.exe no projeto

# 3. Executar START_DEV.bat
# Duplo clique no arquivo

# 4. Copiar URL do ngrok
# Vira algo como: https://abc123.ngrok.io

# 5. Registrar em CN Pay
# CN Pay Dashboard > Integrações > Webhooks

# 6. Testar
# Criar PIX e receber webhook
```

---

## ✅ Checklist

- [ ] ngrok instalado
- [ ] ngrok.exe no diretório do projeto
- [ ] START_DEV.bat funcionando
- [ ] Browser abrindo em localhost:5000
- [ ] ngrok mostrando URL pública
- [ ] Webhook registrado em CN Pay
- [ ] Teste de webhook funcionando

---

**Próximo passo**: Duplo clique em `START_DEV.bat` e teste! 🚀

---

**Versão**: 1.0  
**Data**: 03/02/2026
