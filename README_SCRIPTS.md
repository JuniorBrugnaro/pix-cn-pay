# 🚀 Scripts de Inicialização - PIX CNPAY

**Data**: 03/02/2026

Três formas diferentes de iniciar o projeto em desenvolvimento.

---

## 📋 Arquivos Disponíveis

### 1️⃣ **START_DEV.bat** ⭐ Recomendado (Windows)

**Para quem quer**: Máxima simplicidade, tudo automático

**Como usar**:
1. Abra Explorador de Arquivos
2. Navegue até: `c:\Users\Administrator\Desktop\PIX CNPAY`
3. **Duplo clique** em `START_DEV.bat`

**O que faz**:
- ✅ Ativa virtual environment
- ✅ Inicia ngrok em janela separada
- ✅ Inicia Flask em janela separada
- ✅ Abre browser em `http://localhost:5000`

**Resultado**:
- 3 janelas abertas
- Flask rodando: `http://localhost:5000`
- ngrok rodando: mostra URL pública
- Browser já aberto

---

### 2️⃣ **START_DEV.ps1** (PowerShell - Avançado)

**Para quem quer**: Mais controle, logs detalhados

**Como usar**:

**Opção A** (Direto do PowerShell):
```powershell
powershell -ExecutionPolicy Bypass -File START_DEV.ps1
```

**Opção B** (Se .ps1 estiver associado, duplo clique):
```
START_DEV.ps1
```

**Requisitos**:
- PowerShell Core ou Windows PowerShell 5.0+
- ExecutionPolicy permite scripts

**Vantagens**:
- Logs coloridos
- Detecção automática de URL ngrok
- Encerrando script = encerra ngrok automaticamente

---

### 3️⃣ **START_LOCAL.bat** (Sem ngrok - Testes Simples)

**Para quem quer**: Apenas localhost, sem webhooks remotos

**Como usar**:
1. **Duplo clique** em `START_LOCAL.bat`

**O que faz**:
- ✅ Ativa virtual environment
- ✅ Inicia Flask
- ✅ Pronto para testar em `http://localhost:5000`

**Quando usar**:
- Testes locais simples
- Sem necessidade de webhooks
- ngrok não instalado

---

## 🎯 Comparação Rápida

| Feature | START_DEV.bat | START_DEV.ps1 | START_LOCAL.bat |
|---------|---|---|---|
| Simplicidade | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| ngrok Automático | ✅ | ✅ | ❌ |
| Browser Automático | ✅ | ❌ | ❌ |
| Logs Coloridos | ❌ | ✅ | ❌ |
| Controle Total | ❌ | ✅ | ❌ |
| Requer ngrok | ✅ | ✅ | ❌ |

---

## 📋 Checklist Antes de Usar

### Primeiro Uso (Uma Vez)

- [ ] Python 3.8+ instalado
- [ ] Virtual environment criado: `.venv/`
  ```bash
  python -m venv .venv
  ```
- [ ] Dependências instaladas:
  ```bash
  .venv\Scripts\activate
  pip install -r requirements.txt
  ```
- [ ] .env configurado com credenciais CN Pay

### Apenas para ngrok (START_DEV.bat ou .ps1)

- [ ] ngrok instalado
  - Download: https://ngrok.com/download
  - Extraia `ngrok.exe` no diretório do projeto
- [ ] Conta ngrok criada (opcional, para URL fixa)

---

## 🧪 Fluxo de Uso Típico

### Passo 1: Primeira Execução (Setup)

```bash
# Terminal (uma vez)
cd "c:\Users\Administrator\Desktop\PIX CNPAY"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Passo 2: Iniciar Desenvolvimento

**Opção A** (Recomendado - Webhooks com ngrok):
```bash
# Duplo clique em START_DEV.bat
```

**Opção B** (Apenas localhost):
```bash
# Duplo clique em START_LOCAL.bat
```

### Passo 3: Desenvolver

- Browser já aberto em `http://localhost:5000`
- Logs no terminal
- ngrok rodando (se usou START_DEV.bat)

### Passo 4: Parar

- Feche as janelas (Flask, ngrok)
- Ou pressione `Ctrl+C` nos terminais

---

## 🔧 Uso Manual (Sem Scripts)

Se preferir rodar manualmente:

### Terminal 1: Flask

```bash
cd "c:\Users\Administrator\Desktop\PIX CNPAY"
.venv\Scripts\activate
python app.py
```

Abre em: `http://localhost:5000`

### Terminal 2: ngrok (Opcional)

```bash
cd "c:\Users\Administrator\Desktop\PIX CNPAY"
ngrok http 5000
```

Vira: `https://abc123.ngrok.io`

### Terminal 3: Browser

```bash
start http://localhost:5000
```

---

## ⚠️ Troubleshooting

### Erro: "Arquivo .bat não funciona"

**Solução**: 
- Verifique se está no diretório correto
- Abra PowerShell e tente:
  ```bash
  & ".\START_DEV.bat"
  ```

### Erro: "Virtual environment não ativado"

**Solução**:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Erro: "ngrok não encontrado"

**Solução**:
1. Download: https://ngrok.com/download
2. Extraia `ngrok.exe` no diretório do projeto
3. Verifique:
   ```bash
   ngrok --version
   ```

### Erro: "Porta 5000 já em uso"

**Solução 1**: Feche outra instância Flask
```bash
# Ou mude de porta em .env:
PORT=5001
```

**Solução 2**: Use netstat para encontrar processo
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Browser não abre (START_DEV.bat)

- Funcionalidade do Windows, pode não abrir em alguns PCs
- Abra manualmente: `http://localhost:5000`

---

## 📱 Após Iniciar

### Acessar Aplicação

- **Local**: http://localhost:5000
- **Criar PIX**: POST `/api/create-pix`
- **Verificar**: GET `/api/check-payment/{id}`
- **Webhook**: POST `/webhook`

### Usar ngrok (Se ativado)

- **URL Pública**: Verifique na janela ngrok
- **Dashboard**: http://127.0.0.1:4040
- **Registrar em CN Pay**: Use URL ngrok + `/webhook`

---

## 📝 Notas

- Scripts Windows (.bat) funcionam melhor em CMD/PowerShell nativo
- Scripts PowerShell (.ps1) requerem ExecutionPolicy
- ngrok é opcional (não precisa para testes locais simples)
- URLs ngrok mudam a cada reinicialização (sem conta)

---

## ✅ Próximos Passos

1. Escolha um script (recomendo START_DEV.bat)
2. Duplo clique para iniciar
3. Browser abre automaticamente
4. Teste criar PIX: POST `/api/create-pix`
5. Consulte [PRÓXIMOS_PASSOS.md](PRÓXIMOS_PASSOS.md) para guias detalhados

---

**Versão**: 1.0  
**Data**: 03/02/2026

