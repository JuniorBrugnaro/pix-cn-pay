# 🚀 Checkout PIX - CN Pay Integration

Sistema completo de checkout com geração de PIX utilizando a API da CN Pay, desenvolvido em **Python Flask** com deploy no **Render**.

## 📦 Arquivos do Projeto

```
checkout-pix-cnpay/
├── app.py                          # Aplicação Flask (backend)
├── requirements.txt                # Dependências Python
├── Procfile                        # Configuração Render
├── render.yaml                     # Build config Render
├── .env                           # Variáveis de ambiente (local)
├── .gitignore                     # Arquivos ignorados pelo Git
├── templates/
│   └── checkout.html              # Template do checkout
├── DOCUMENTACAO_CNPAY.md          # Documentação completa da API
├── README_DEPLOY.md               # Guia completo de deploy no Render
├── test_local.py                  # Script de teste local
└── README.md                      # Este arquivo
```

## ✨ Funcionalidades

### Frontend
- ✅ Interface moderna e responsiva
- ✅ Seleção de valores pré-definidos (R$ 10 a R$ 50)
- ✅ Campo para valor personalizado
- ✅ Geração de QR Code PIX em tempo real
- ✅ Código PIX copia e cola
- ✅ Verificação automática de pagamento
- ✅ Status em tempo real
- ✅ Animações e feedback visual

### Backend (Python Flask)
- ✅ API REST completa
- ✅ Integração com CN Pay API
- ✅ Endpoint para criar PIX
- ✅ Endpoint para consultar status
- ✅ Webhook para receber notificações
- ✅ Health check para monitoramento
- ✅ Logs detalhados
- ✅ Tratamento de erros robusto
- ✅ Pronto para deploy no Render
- ✅ Segurança: credenciais no backend

## 🎨 Preview

O checkout possui:
- Design fiel ao original com melhorias de UX
- Cores: Vermelho (#ef4444) como cor principal
- Gradientes suaves e animações profissionais
- Responsivo para mobile e desktop
- Feedback visual em todas as interações

## 🚀 Como Usar

### 🔥 Opção 1: Deploy no Render (Recomendado)

**Veja o guia completo:** [README_DEPLOY.md](README_DEPLOY.md)

**Resumo rápido:**

1. **Criar repositório no GitHub**
   - Faça upload de todos os arquivos
   - Não envie o `.env`!

2. **Criar Web Service no Render**
   - Conecte o repositório
   - Configure variáveis de ambiente
   - Deploy automático!

3. **Acessar aplicação**
   - URL: `https://seu-app.onrender.com`
   - Pronto para usar! 🎉

### 💻 Opção 2: Rodar Localmente

#### Requisitos
- Python 3.8+
- pip

#### Instalação

```bash
# 1. Clone ou baixe os arquivos
cd checkout-pix-cnpay

# 2. Crie um ambiente virtual (opcional mas recomendado)
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
# Edite o arquivo .env com suas credenciais

# 5. Execute a aplicação
python app.py
```

#### Ou use o script de teste:

```bash
python test_local.py
```

O script irá:
- ✅ Verificar Python e arquivos
- ✅ Instalar dependências (se necessário)
- ✅ Executar testes básicos
- ✅ Iniciar o servidor

#### Acessar

Abra o navegador em: `http://localhost:5000`

## 🔔 Configurar Webhook

### Passo 1: Deploy no Render

Primeiro faça o deploy para obter a URL do seu app:
```
https://seu-app.onrender.com
```

### Passo 2: Configurar no Painel CN Pay

1. Acesse: https://painel.appcnpay.com
2. Vá em: Configurações > Webhooks
3. Clique em "Criar"
4. Configure:
   - **Título:** Webhook Pushin Pay
   - **URL:** `https://seu-app.onrender.com/webhook`
   - **Eventos:** 
     - ✅ TRANSACTION_PAID
     - ✅ TRANSACTION_CREATED
     - ✅ TRANSACTION_CANCELED
     - ✅ TRANSACTION_REFUNDED

### Passo 3: Atualizar Variável no Render

1. No Render, vá em seu serviço
2. Clique em "Environment"
3. Adicione:
   - **Key:** `WEBHOOK_URL`
   - **Value:** `https://seu-app.onrender.com/webhook`
4. Salve (serviço reiniciará automaticamente)

### Como Funciona

Quando um pagamento é confirmado:
```
Cliente paga PIX
    ↓
CN Pay detecta pagamento
    ↓
CN Pay envia POST /webhook
    ↓
Seu servidor recebe notificação
    ↓
Você libera produto/serviço
```

## 📡 API Endpoints

### POST /api/create-pix

Criar cobrança PIX

**Request:**
```json
{
  "amount": 25.00,
  "client": {
    "name": "Cliente",
    "email": "cliente@email.com",
    "phone": "11999999999"
  }
}
```

**Response:**
```json
{
  "success": true,
  "transactionId": "xa69kbub2c",
  "identifier": "PIX_1738616400000_abc123",
  "status": "PENDING",
  "pix": {
    "qrCode": "00020126...",
    "image": "https://..."
  }
}
```

### GET /api/check-payment/:transactionId

Consultar status do pagamento

**Response:**
```json
{
  "success": true,
  "transaction": {
    "id": "xa69kbub2c",
    "status": "COMPLETED",
    "amount": 25.00,
    "payedAt": "2026-02-03T22:25:05.166Z"
  }
}
```

### POST /webhook

Receber notificações da CN Pay (configurado automaticamente)

## 🔍 Verificação de Status

O checkout verifica o status automaticamente a cada 5 segundos usando:

```javascript
GET /gateway/transactions?id={transactionId}
```

**Status possíveis:**
- `PENDING` - Aguardando pagamento
- `COMPLETED` - Pagamento confirmado ✅
- `FAILED` - Pagamento falhou ❌
- `REFUNDED` - Estornado

## 🛡️ Segurança

### ⚠️ NUNCA faça isso em produção:

```javascript
// ❌ NÃO exponha credenciais no frontend
const secretKey = 'c3qfmxlk7iw147u7g5b47l2u7eghbd6vi3sgsb908afhrcvh2tqsksoxi7zyr75e';
```

### ✅ Faça isso:

1. **Backend intermediário:**

```javascript
// Frontend chama seu backend
fetch('/api/create-pix', {
    method: 'POST',
    body: JSON.stringify({ amount: 25 })
});

// Backend chama CN Pay
// server.js
app.post('/api/create-pix', async (req, res) => {
    const response = await fetch('https://painel.appcnpay.com/api/v1/gateway/pix/receive', {
        headers: {
            'x-public-key': process.env.CNPAY_PUBLIC_KEY,
            'x-secret-key': process.env.CNPAY_SECRET_KEY
        },
        body: JSON.stringify({...})
    });
    
    const data = await response.json();
    res.json(data);
});
```

2. **Variáveis de ambiente:**

```bash
# .env (exemplo)
CNPAY_PUBLIC_KEY=financeiro_moqjrint4j9xhzzt
CNPAY_SECRET_KEY=c3qfmxlk7iw147u7g5b47l2u7eghbd6vi3sgsb908afhrcvh2tqsksoxi7zyr75e
# URL da API (opcional)
CNPAY_API_URL=https://painel.appcnpay.com/api/v1
# Webhook
WEBHOOK_URL=https://seu-app.onrender.com/webhook
WEBHOOK_SECRET=um-token-secreto-para-validar-webhooks
# CORS (origens permitidas, separadas por vírgula) - opcional
# Exemplo: CORS_ORIGINS=https://meusite.com,https://admin.meusite.com
CORS_ORIGINS='https://seu-site.com'
# Ative DEBUG apenas em desenvolvimento
DEBUG=False
```

Observações:
- `WEBHOOK_SECRET` é usado para validar que os POSTs recebidos no endpoint `/webhook` vêm da CN Pay.
- `CORS_ORIGINS` permite restringir as origens que podem chamar os endpoints `-/api/*` (recomendado em produção).
- Nunca comite o arquivo `.env` no repositório.
- Consulte `SECURITY.md` para práticas de segurança e instruções de auditoria de dependências.

## 🧪 Testes

### 1. Ambiente de Desenvolvimento

```bash
# Usar valores baixos para teste
Testar com: R$ 0,01, R$ 0,50, R$ 1,00
```

### 2. Verificar Logs

Abra o console do navegador (F12) para ver:
- Requisições à API
- Respostas recebidas
- Erros (se houver)

### 3. Testar Webhook

Use ferramentas como:
- [ngrok](https://ngrok.com) - Para expor localhost
- [webhook.site](https://webhook.site) - Para receber webhooks de teste

```bash
# Expor localhost com ngrok
ngrok http 3000

# Copiar URL gerada e configurar no painel CN Pay
https://abc123.ngrok.io/webhook/cnpay
```

## 📚 Documentação Adicional

### Arquivos Incluídos

- **DOCUMENTACAO_CNPAY.md** - Documentação completa da API
  - Todos os endpoints
  - Estruturas de request/response
  - Códigos de erro
  - Exemplos práticos

- **webhook-server-example.js** - Servidor webhook pronto
  - Implementação completa em Node.js
  - Handlers para todos os eventos
  - Exemplos comentados
  - Suporte a TypeScript

## ⚡ Próximos Passos

- [ ] 1. Testar checkout em ambiente local
- [ ] 2. Fazer um pagamento de teste (R$ 0,50)
- [ ] 3. Configurar webhook no painel CN Pay
- [ ] 4. Implementar servidor webhook
- [ ] 5. Testar fluxo completo
- [ ] 6. Mover credenciais para backend
- [ ] 7. Adicionar validações extras
- [ ] 8. Implementar logs e monitoramento
- [ ] 9. Fazer testes de carga
- [ ] 10. Deploy em produção

## 🔧 Customização

### Alterar Valores Pré-definidos

No arquivo `checkout-pix-cnpay.html`:

```html
<button class="amount-btn" data-amount="10">10</button>
<button class="amount-btn" data-amount="20">20</button>
<!-- Adicione mais valores aqui -->
<button class="amount-btn" data-amount="100">100</button>
```

### Alterar Cores

```css
/* Cor principal (vermelho) */
.header {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

/* Altere para outra cor, exemplo azul: */
.header {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}
```

### Alterar Textos

```html
<h1>GERADOR PIX</h1>
<p>PUSHIN PAY - KIVORA</p>
```

## ❓ Problemas Comuns

### 1. Erro CORS

**Problema:** Erro de CORS ao chamar a API

**Solução:** Implemente backend intermediário (veja seção Segurança)

### 2. Credenciais Inválidas

**Problema:** Erro `GATEWAY_UNAUTHORIZED`

**Solução:** Verifique se as chaves estão corretas no código

### 3. QR Code não aparece

**Problema:** QR Code não é exibido

**Solução:** Verifique se a API retornou `pix.qrCode` na resposta

### 4. Status não atualiza

**Problema:** Status fica sempre em "Aguardando"

**Solução:** 
- Verifique se o `transactionId` está correto
- Confirme que o pagamento foi feito
- Veja logs do console (F12)

## 📞 Suporte CN Pay

- **Documentação:** https://painel.appcnpay.com/docs
- **Email:** contato@appcnpay.com
- **Painel:** https://painel.appcnpay.com

## 📄 Licença

Este projeto é de uso livre. Desenvolvido com ❤️ por Claude.

---

**Versão:** 2.0.0  
**Última atualização:** 03/02/2026  
**Desenvolvido para:** Pushin Pay - Kivora
