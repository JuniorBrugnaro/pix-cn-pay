# 🚀 Guia de Deploy no Render

## 📋 Pré-requisitos

- Conta no GitHub
- Conta no Render (gratuita)
- Arquivos do projeto prontos

## 📁 Estrutura do Projeto

```
checkout-pix-cnpay/
├── app.py                    # Aplicação Flask principal
├── requirements.txt          # Dependências Python
├── Procfile                  # Comando de inicialização
├── render.yaml              # Configuração do Render
├── .env                     # Variáveis de ambiente (local)
├── templates/
│   └── checkout.html        # Template do checkout
└── README_DEPLOY.md         # Este arquivo
```

## 🔧 Passo 1: Preparar Repositório GitHub

### 1.1 Criar Repositório

1. Acesse: https://github.com/new
2. Nome: `checkout-pix-cnpay` (ou outro nome)
3. Privacidade: Public ou Private
4. Clique em "Create repository"

### 1.2 Fazer Upload dos Arquivos

**Opção A: Via GitHub Web Interface**

1. Clique em "uploading an existing file"
2. Arraste todos os arquivos:
   - `app.py`
   - `requirements.txt`
   - `Procfile`
   - `render.yaml`
   - Pasta `templates/` com `checkout.html`
3. Commit: "Initial commit"
4. Clique em "Commit changes"

**Opção B: Via Git CLI**

```bash
# No terminal, dentro da pasta do projeto
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/checkout-pix-cnpay.git
git push -u origin main
```

⚠️ **IMPORTANTE:** Não faça upload do arquivo `.env` para o GitHub!

## 🌐 Passo 2: Fazer Deploy no Render

### 2.1 Criar Web Service

1. Acesse: https://render.com
2. Clique em "New +" > "Web Service"
3. Conecte sua conta GitHub se ainda não conectou
4. Selecione o repositório `checkout-pix-cnpay`
5. Clique em "Connect"

### 2.2 Configurar Web Service

Preencha os campos:

**Name:** `checkout-pix-cnpay` (ou outro nome único)

**Region:** `Oregon (US West)` (mais próximo do Brasil é Ohio)

**Branch:** `main`

**Root Directory:** (deixe vazio)

**Runtime:** `Python 3`

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn app:app
```

**Instance Type:** `Free` (para testes)

### 2.3 Configurar Variáveis de Ambiente

Clique em "Advanced" e adicione as seguintes variáveis:

| Key | Value |
|-----|-------|
| `CNPAY_PUBLIC_KEY` | `financeiro_moqjrint4j9xhzzt` |
| `CNPAY_SECRET_KEY` | `c3qfmxlk7iw147u7g5b47l2u7eghbd6vi3sgsb908afhrcvh2tqsksoxi7zyr75e` |
| `CNPAY_API_URL` | `https://painel.appcnpay.com/api/v1` |
| `FLASK_ENV` | `production` |
| `DEBUG` | `False` |

**Webhook URL** (adicionar depois):
- Deixe em branco por enquanto
- Será configurado no Passo 4

### 2.4 Fazer Deploy

1. Clique em "Create Web Service"
2. Aguarde o build (3-5 minutos)
3. Status deve ficar "Live" quando pronto

## 🎉 Passo 3: Acessar a Aplicação

Após o deploy bem-sucedido:

1. Render fornecerá uma URL: `https://checkout-pix-cnpay.onrender.com`
2. Acesse a URL no navegador
3. Você verá o checkout funcionando!

## 🔔 Passo 4: Configurar Webhook (Opcional)

### 4.1 Obter URL do Webhook

Sua URL do webhook será:
```
https://SEU-APP.onrender.com/webhook
```

Exemplo:
```
https://checkout-pix-cnpay.onrender.com/webhook
```

### 4.2 Configurar no Painel CN Pay

1. Acesse: https://painel.appcnpay.com
2. Vá em: Configurações > Webhooks
3. Clique em "Criar webhook"
4. Preencha:
   - **Título:** Webhook Pushin Pay
   - **URL alvo:** `https://SEU-APP.onrender.com/webhook`
   - **Eventos:** Selecione todos ou específicos:
     - TRANSACTION_CREATED
     - TRANSACTION_PAID
     - TRANSACTION_CANCELED
     - TRANSACTION_REFUNDED
5. Salve

### 4.3 Atualizar Variável de Ambiente no Render

1. No Render, vá em seu serviço
2. Clique em "Environment"
3. Adicione nova variável:
   - **Key:** `WEBHOOK_URL`
   - **Value:** `https://SEU-APP.onrender.com/webhook`
4. Clique em "Save Changes"
5. O serviço será reiniciado automaticamente

## 🧪 Passo 5: Testar

### 5.1 Testar Checkout

1. Acesse: `https://SEU-APP.onrender.com`
2. Selecione um valor (ex: R$ 0,50)
3. Clique em "Gerar PIX"
4. Verifique se o QR Code aparece
5. Copie o código PIX

### 5.2 Testar Pagamento

1. Abra seu app do banco
2. Vá em PIX > Pix Copia e Cola
3. Cole o código
4. Faça o pagamento
5. Aguarde 5-10 segundos
6. O status deve atualizar para "Pagamento confirmado"

### 5.3 Verificar Logs

Para ver os logs da aplicação:

1. No Render, clique em "Logs"
2. Você verá:
   - Requisições recebidas
   - PIX criados
   - Webhooks recebidos
   - Erros (se houver)

## 📊 Monitoramento

### Health Check

Render verifica automaticamente se a aplicação está funcionando através do endpoint:
```
GET https://SEU-APP.onrender.com/health
```

Resposta esperada:
```json
{
  "status": "ok",
  "timestamp": "2026-02-03T...",
  "service": "checkout-pix-cnpay"
}
```

## 🔄 Atualizações

### Como Atualizar a Aplicação

**Opção 1: Via GitHub Web**
1. Edite os arquivos no GitHub
2. Faça commit
3. Render faz deploy automático

**Opção 2: Via Git CLI**
```bash
# Fazer mudanças nos arquivos
git add .
git commit -m "Descrição das mudanças"
git push origin main
# Render faz deploy automático
```

### Forçar Redeploy Manual

1. No Render, vá em seu serviço
2. Clique em "Manual Deploy" > "Deploy latest commit"

## ⚙️ Configurações Avançadas

### Custom Domain

1. No Render: Settings > Custom Domains
2. Adicione seu domínio
3. Configure DNS conforme instruções

### HTTPS

- Render fornece HTTPS automático
- Certificado SSL gratuito via Let's Encrypt

### Escalabilidade

Free tier do Render:
- ✅ 512 MB RAM
- ✅ 0.1 CPU
- ✅ HTTPS automático
- ⚠️ Dorme após 15 min de inatividade
- ⚠️ 750 horas/mês grátis

Para evitar que durma:
- Upgrade para plano pago ($7/mês)
- Use serviço de ping (ex: UptimeRobot)

## 🐛 Problemas Comuns

### 1. Build Failed

**Erro:** `Could not find a version that satisfies the requirement`

**Solução:** Verifique `requirements.txt`:
```txt
Flask==3.0.0
Flask-Cors==4.0.0
requests==2.31.0
gunicorn==21.2.0
python-dotenv==1.0.0
```

### 2. Application Error

**Erro:** Tela branca ou erro 500

**Solução:**
1. Verifique os logs no Render
2. Confirme que todas as variáveis de ambiente estão configuradas
3. Verifique se `Procfile` está correto

### 3. Webhook Não Funciona

**Erro:** Pagamentos não atualizam automaticamente

**Solução:**
1. Confirme que `WEBHOOK_URL` está configurado
2. Verifique se a URL está correta no painel CN Pay
3. Veja os logs para confirmar se o webhook está sendo recebido

### 4. CORS Error

**Erro:** Blocked by CORS policy

**Solução:** Já está configurado no `app.py` com `Flask-Cors`

## 📞 Suporte

**Render:**
- Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

**CN Pay:**
- Docs: https://painel.appcnpay.com/docs
- Email: contato@appcnpay.com

## ✅ Checklist Final

- [ ] Repositório GitHub criado
- [ ] Arquivos enviados para GitHub
- [ ] Web Service criado no Render
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy bem-sucedido (status "Live")
- [ ] Aplicação acessível via URL
- [ ] Teste de criação de PIX funcionando
- [ ] Webhook configurado (se usar)
- [ ] Teste de pagamento completo realizado
- [ ] Logs monitorados e funcionais

## 🎯 Próximos Passos

1. [ ] Personalizar design conforme sua marca
2. [ ] Adicionar banco de dados (PostgreSQL)
3. [ ] Implementar autenticação de usuários
4. [ ] Criar painel administrativo
5. [ ] Configurar domínio personalizado
6. [ ] Implementar analytics
7. [ ] Adicionar mais métodos de pagamento

---

**Versão:** 1.0.0  
**Última atualização:** 03/02/2026  
**Desenvolvido para:** Pushin Pay - Kivora
