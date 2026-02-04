# Relatório de Análise - Documentação CN Pay vs Código

**Data**: 03/02/2026  
**Status**: Análise consolidada

---

## 📋 Resumo Executivo

A análise da documentação oficial CN Pay revelou **pontos críticos de integração** que precisam de validação contra o código atual. O webhook e os endpoints de criação/verificação de PIX foram os focos principais.

---

## 🔍 Descobertas Críticas

### 1. **Webhook - Formato e Token Validation**

#### O que a Documentação diz:
- **Arquivo**: `Pagamentos _ Documentação CN Pay.pdf`
- **URL docs**: https://painel.appcnpay.com/docs/webhooks
- **Formato esperado do payload webhook**:
  ```json
  {
    "event": "nome do evento",
    "token": "token gerado para validação",
    "offerCode": "Código da oferta quando é venda no checkout interno",
    "client": {
      "id": "identificador do cliente",
      "name": "nome do cliente",
      "email": "email do cliente",
      "phone": "telefone do cliente",
      "cpf": "CPF do cliente", // ou null
      "cnpj": "CNPJ do cliente", // ou null
      "address": { /* ... */ }
    },
    "transaction": {
      "id": "identificador da transação",
      "identifier": "Seu identificador da transação",
      "status": "status da transação",
      "paymentMethod": "método de pagamento",
      "originalCurrency": "moeda do cliente",
      "originalAmount": "valor na moeda do cliente",
      "currency": "sua moeda de recebimento",
      "amount": "valor na sua moeda de recebimento",
      "createdAt": "data e hora de criação",
      "payedAt": "data e hora do pagamento",
      "pixInformation": {
        "qrCode": "string com QR code PIX",
        "endToEndId": "ID fim-a-fim da transação PIX"
      }
    },
    "subscription": null, // null quando não é assinatura
    "items": [ /* ... */ ]
  }
  ```

#### Status Atual do Código:
- ✅ Token validation está implementado em `/webhook`
- ✅ Webhook recebe POST com JSON
- ⚠️ **Verificar**: O token é comparado com `WEBHOOK_SECRET` — precisa confirmar se a CN Pay envia o token esperado

#### ✅ Recomendação
- Código está alinhado
- Manter validação de token
- Logar eventos webhook (mascarar token nos logs)

---

### 2. **Endpoint CREATE PIX - `POST /gateway/pix/receive`**

#### O que a Documentação diz:
- **Arquivo**: `Receber pix _ Documentação CN Pay.pdf`
- **Endpoint**: `POST /gateway/pix/receive` (autenticado)
- **Campos OBRIGATÓRIOS**:
  ```json
  {
    "identifier": "Identificador único da transação (criado pela aplicação)",
    "amount": "Valor da transação em reais (numérico)"
  }
  ```
- **Campos OPCIONAIS**:
  - `shippingFee`: Frete em reais
  - `extraFee`: Outras taxas em reais
  - `client`: Dados do cliente
  - `products`: Array de produtos
  - `callbackUrl`: URL para webhooks

#### Status Atual do Código:
- ✅ Endpoint correto: `/gateway/pix/receive`
- ✅ Identifier único gerado: `generate_identifier()`
- ✅ Amount validado como float
- ✅ Callback URL adicionada ao payload
- ✅ Headers com `x-public-key` e `x-secret-key`

#### ✅ Recomendação
- Código está alinhado com documentação

---

### 3. **Endpoint CHECK PAYMENT - `GET /gateway/transactions`**

#### O que a Documentação diz:
- **Arquivo**: `Buscar transação _ Documentação CN Pay.pdf`
- **Endpoint**: `GET /gateway/transactions` (autenticado)
- **Query Parameters**:
  ```
  ?id=<ID_DA_TRANSAÇÃO>       (retornado pela API ao criar)
  &clientIdentifier=<SEU_ID>  (seu identifier enviado na criação)
  ```
- **Retorno 200 OK** inclui:
  - `id`: ID da transação
  - `clientIdentifier`: Seu identificador enviado
  - `status`: Status atual
  - `pixInformation.qrCode`: String com QR code
  - `pixInformation.base64`: Imagem em base64

#### Status Atual do Código:
- ✅ Endpoint correto: `/gateway/transactions`
- ✅ Query parameters com `id` e `clientIdentifier`
- ✅ Response parsing para retornar `qrCode` e `base64`

#### ✅ Recomendação
- Código está alinhado com documentação

---

### 4. **Erro Handling - `Tratamento de erros`**

#### O que a Documentação diz:
- **Arquivo**: `Tratamento de erros _ Documentação CN Pay.pdf`
- **Formato do erro**:
  ```json
  {
    "statusCode": 500,
    "errorCode": "GATEWAY_INTERNAL_SERVER_ERROR",
    "message": "Mensagem detalhada sobre o erro",
    "details": {
      "campo1": "Detalhes sobre o campo 1",
      "campo2": "Detalhes sobre o campo 2"
    }
  }
  ```

#### Status Atual do Código:
- ✅ Retorna status HTTP correto
- ✅ Retorna JSON com `success` e `error`
- ✅ Details visíveis apenas em DEBUG mode
- ⚠️ **Melhoria**: Poderia incluir `errorCode` padronizado

#### ⚠️ Recomendação (Opcional)
- Adicionar campo `errorCode` em respostas de erro (exemplo: `PIX_INVALID_AMOUNT`)
- Isso facilita debugging e logging estruturado

---

## 📊 Matriz de Validação

| Feature | Docs | Código | Status | Observações |
|---------|------|--------|--------|------------|
| POST /gateway/pix/receive | ✅ | ✅ | ✅ OK | Alinhado |
| GET /gateway/transactions | ✅ | ✅ | ✅ OK | Alinhado |
| Webhook token validation | ✅ | ✅ | ✅ OK | Alinhado |
| Webhook payload format | ✅ | ✅ | ✅ OK | Alinhado (recebe e processa) |
| Error handling | ✅ | ⚠️ | ⚠️ Parcial | Funciona, mas poderia ser mais estruturado |
| Autenticação headers | ✅ | ✅ | ✅ OK | x-public-key, x-secret-key presentes |

---

## 🚀 Ações Recomendadas

### **Prioridade 🔴 ALTA**
- [ ] **Testes de integração em sandbox CN Pay**
  - Validar payload completo
  - Confirmar formato webhook recebido
  - Testar error scenarios

### **Prioridade 🟡 MÉDIA**
- [ ] **Adicionar código de erro padronizado** (exemplo: `PIX_INVALID_AMOUNT`, `WEBHOOK_VALIDATION_FAILED`)
- [ ] **Melhorar logging estruturado** com event tracking

### **Prioridade 🟢 BAIXA**
- [ ] **Documentar casos de erro** esperados (timeout, rate limit, etc.)
- [ ] **Adicionar retry logic** para falhas transitórias

---

## 📝 Conclusão

✅ **O código está bem alinhado com a documentação CN Pay.**

Os endpoints, campos obrigatórios, autenticação e tratamento de webhooks estão implementados corretamente. 

**Próximo passo crítico**: Executar testes em sandbox antes de deployar em produção.

---

**Gerado por**: Análise automática de documentação  
**Versão app.py**: Última versão (com hardening aplicado)
