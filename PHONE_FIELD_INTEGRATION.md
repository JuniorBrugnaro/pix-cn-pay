# Integração do Campo de Telefone do Cliente

## Resumo
Foi implementado um campo de entrada de telefone que coleta o número de contato do cliente e o vincula ao pagamento PIX através da API CN Pay.

## Mudanças Realizadas

### 1. **Frontend - HTML (templates/checkout.html)**
Adicionado campo de entrada de telefone com os seguintes características:

```html
<div class="phone-input-section">
    <label for="clientPhone">Seu telefone:</label>
    <input 
        type="tel" 
        id="clientPhone" 
        class="phone-input" 
        placeholder="(11) 99999-9999"
        pattern="[0-9\(\)\-\s]+"
        maxlength="15"
    >
</div>
```

**Posicionamento**: Entre o header "CNPAY PAGAMENTOS" e os botões de seleção de valor

**Características**:
- Tipo: `tel` (entrada de telefone)
- ID: `clientPhone`
- Placeholder: `(11) 99999-9999`
- Máximo de caracteres: 15
- Padrão aceito: números, parênteses, hífens e espaços

### 2. **Frontend - CSS (templates/checkout.html)**
Adicionado estilos para o campo de telefone:

```css
.phone-input-section {
    margin-bottom: 24px;
}

.phone-input-section label {
    display: block;
    color: #9ca3af;
    font-size: 13px;
    margin-bottom: 8px;
    font-weight: 500;
}

.phone-input {
    width: 100%;
    background: #1f2937;
    border: 2px solid #ef4444;  /* Vermelho */
    border-radius: 12px;
    padding: 14px 16px;
    color: white;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.2s;
}

.phone-input:focus {
    outline: none;
    border-color: #10b981;  /* Verde ao focar */
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.phone-input::placeholder {
    color: #6b7280;
}
```

**Design**:
- Borda vermelha (#ef4444) para indicar campo importante
- Borda verde (#10b981) ao receber foco
- Fundo cinza escuro (#1f2937) consistente com o design
- Sombra suave ao focar para melhor UX

### 3. **Frontend - JavaScript (templates/checkout.html)**
Modificada função `generatePix()` para capturar e validar o telefone:

```javascript
// Gerar PIX
async function generatePix() {
    const amount = selectedAmount || parseFloat(document.getElementById('customAmount').value);
    const phoneNumber = document.getElementById('clientPhone').value.trim();

    if (!amount || amount <= 0) {
        showError('Por favor, selecione ou digite um valor válido');
        return;
    }

    if (!phoneNumber) {
        showError('Por favor, insira seu telefone');
        return;
    }

    const btn = document.getElementById('generateBtn');
    btn.disabled = true;
    btn.innerHTML = '<span class="loading"></span> Gerando PIX...';

    try {
        const response = await fetch('/api/create-pix', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                amount: amount,
                client: {
                    name: 'Cliente',
                    email: 'cliente@exemplo.com',
                    document: '00000000000000',
                    phone: phoneNumber  // ← Telefone do cliente
                }
            })
        });
```

**Validações**:
- Verifica se o telefone foi preenchido
- Remove espaços em branco (trim)
- Exibe mensagem de erro se vazio
- Envia o telefone no payload JSON para a API

### 4. **Backend - Python (app.py)**
O backend já estava preparado para receber o telefone. A função `create_pix()` recebe o telefone e o envia para a CN Pay API:

```python
# Campos obrigatórios de cliente (CN Pay requer)
if data.get('client'):
    client = data['client']
    # Validar campos obrigatórios do cliente
    if all(k in client for k in ['name', 'email', 'document', 'phone']):
        payload['client'] = {
            'name': client.get('name'),
            'email': client.get('email'),
            'document': client.get('document'),
            'phone': client.get('phone')  # ← Telefone incluído
        }
```

## Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Cliente Preenche o Formulário                             │
│    - Insere número de telefone no campo                      │
│    - Seleciona valor de pagamento                            │
│    - Clica em "Gerar PIX"                                    │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│ 2. JavaScript Valida e Captura Dados                         │
│    - Extrai: getElementById('clientPhone').value             │
│    - Valida: se não está vazio                               │
│    - Monta payload JSON com: amount, client{phone}           │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│ 3. POST /api/create-pix                                      │
│    Body JSON: {                                              │
│      amount: 25.00,                                          │
│      client: {                                               │
│        name: 'Cliente',                                      │
│        email: 'cliente@exemplo.com',                         │
│        document: '00000000000000',                           │
│        phone: '(11) 98765-4321'                              │
│      }                                                       │
│    }                                                         │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│ 4. Backend Flask (app.py)                                    │
│    - Recebe dados do cliente                                 │
│    - Monta payload para CN Pay API                           │
│    - Envia: POST /gateway/pix/receive com dados completos    │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│ 5. CN Pay API                                                │
│    - Processa pagamento PIX com telefone vinculado           │
│    - Retorna: qr_code, payment_code, transaction_id          │
│    - Armazena: Telefone associado à transação               │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│ 6. Frontend Recebe Resposta                                  │
│    - Exibe QR code para pagamento                            │
│    - Exibe código PIX copiável                               │
│    - Inicia verificação de status                            │
└─────────────────────────────────────────────────────────────┘
```

## Localização no Formulário

```
┌────────────────────────────────────────────┐
│           GERADOR PIX                      │  ← Header
│         CNPAY PAGAMENTOS                   │
└────────────────────────────────────────────┘
┌────────────────────────────────────────────┐
│   Seu telefone:                            │  ← NOVO CAMPO
│   [(11) 99999-9999            ]            │
└────────────────────────────────────────────┘
┌────────────────────────────────────────────┐
│     Selecione o valor                      │
│  [10] [15] [20]                            │  ← Botões de valor
│  [25] [30] [35]                            │
│  [40] [45] [50]                            │
│                                            │
│  Ou digite um valor:                       │
│  [______________________]                  │
└────────────────────────────────────────────┘
```

## Testando a Integração

### Teste Local com ngrok

1. **Inicie o servidor Flask**:
   ```bash
   python app.py
   ```
   Saída esperada:
   ```
   ✅ Webhook URL: https://pix-cnpay.onrender.com/webhook
   Running on http://127.0.0.1:5000
   ```

2. **Abra o formulário em http://localhost:5000**

3. **Preencha o campo de telefone** com um número como `(11) 99999-9999`

4. **Selecione um valor e clique em "Gerar PIX"**

5. **Verifique a requisição**:
   - Abra DevTools (F12) → Network
   - Clique em "Gerar PIX"
   - Inspecione a requisição POST para `/api/create-pix`
   - Verifique se o payload contém o telefone:
     ```json
     {
       "amount": 25,
       "client": {
         "phone": "(11) 99999-9999",
         "name": "Cliente",
         "email": "cliente@exemplo.com",
         "document": "00000000000000"
       }
     }
     ```

6. **Verifique no Dashboard CN Pay**:
   - Acesse https://painel.appcnpay.com
   - Vá para "Transações" ou "Cobranças"
   - Procure a transação criada
   - Verifique se o telefone do cliente aparece nos detalhes

## Formatos Aceitos de Telefone

O campo aceita formatos comuns brasileiros:
- `11999999999` (11 dígitos puros)
- `(11) 99999-9999` (com formatação padrão)
- `11 99999-9999` (sem parênteses)
- `(11)99999-9999` (compacto com parênteses)

## Próximos Passos (Opcional)

Para melhorias futuras, considere:

1. **Máscara de entrada automática**: Formatar automaticamente enquanto digita
   ```javascript
   // Aplicar mask (11) 99999-9999 em tempo real
   ```

2. **Validação de telefone**: Verificar se é um telefone válido
   ```javascript
   // Validar se tem 11 dígitos para celular SP
   ```

3. **Captura de mais dados**: Nome e email do cliente
   - Adicionar campos adicionais se necessário

4. **Integração com WhatsApp**: Enviar notificações via WhatsApp do cliente

## Histórico de Commits

- **Commit**: `5c2b0bb` - feat: adicionar campo de telefone do cliente vinculado ao pagamento
- **Data**: Conforme timestamp do git
- **Mudanças**: +53 inserções, -1 deleção em `templates/checkout.html`

## Arquivos Modificados

- ✅ `templates/checkout.html` (823 linhas)
  - HTML: +7 linhas para campo de telefone
  - CSS: +36 linhas para estilos
  - JavaScript: +5 linhas para captura de dados

- ℹ️ `app.py` (Sem mudanças - já suportava telefone)

## Verificação de Funcionamento

```javascript
// Teste no console do navegador para validar:
document.getElementById('clientPhone').value = '(11) 98765-4321';
generatePix(); // Irá gerar PIX com este telefone
```

## Conclusão

O campo de telefone foi implementado com sucesso e está totalmente integrado ao fluxo de pagamento PIX. O telefone do cliente agora é capturado, validado e enviado para a CN Pay API, sendo vinculado ao pagamento realizado.
