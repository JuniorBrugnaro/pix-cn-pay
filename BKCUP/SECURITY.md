# Segurança

Este arquivo descreve práticas e instruções de segurança para este projeto.

## Variáveis de ambiente obrigatórias

Em produção, defina as seguintes variáveis de ambiente (nunca commitá-las):

- `CNPAY_PUBLIC_KEY` — chave pública CN Pay
- `CNPAY_SECRET_KEY` — chave secreta CN Pay
- `WEBHOOK_URL` — URL pública do webhook (ex.: https://seu-app.onrender.com/webhook)
- `WEBHOOK_SECRET` — token/secret usado para validar webhooks recebidos
- `DEBUG` — `False` em produção

O servidor falhará ao iniciar se `CNPAY_PUBLIC_KEY` e `CNPAY_SECRET_KEY` não estiverem presentes e `DEBUG` não estiver ativo.

## Boas práticas

- Nunca inclua credenciais no repositório. Use um gerenciador de segredos (Render env, AWS Secrets Manager, GitHub Secrets).
- Rotacione as chaves periodicamente e imediatamente após qualquer suspeita de vazamento.
- Habilite HTTPS e verifique configurações de TLS no gateway de deploy.
- Valide o `token` do webhook em `WEBHOOK_SECRET` e não confie apenas no IP de origem.
- Não exponha `CNPAY_SECRET_KEY` no frontend.

## Auditoria de dependências

Use `pip-audit` para verificar vulnerabilidades nas dependências:

```bash
pip install pip-audit
pip-audit -r requirements.txt --format json
```

Recomenda-se rodar `pip-audit` no CI (workflow incluído em `.github/workflows/pip-audit.yml`).

## Relatar vulnerabilidades

Se encontrar uma vulnerabilidade neste projeto, abra uma issue privado no repositório (ou envie por e-mail para o mantenedor). Não publique segredos na issue.
