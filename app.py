"""
Aplicação Flask - Checkout PIX CN Pay
Deploy: Render.com
"""

from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from datetime import datetime
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__)

# ==================== CONFIGURAÇÕES ====================
class Config:
    # CN Pay API
    # As chaves devem ser definidas via variáveis de ambiente em produção.
    # Em DEBUG as chaves de exemplo serão usadas para facilitar testes locais.
    CNPAY_PUBLIC_KEY = os.getenv('CNPAY_PUBLIC_KEY')
    CNPAY_SECRET_KEY = os.getenv('CNPAY_SECRET_KEY')
    CNPAY_API_URL = os.getenv('CNPAY_API_URL', 'https://painel.appcnpay.com/api/v1')
    
    # Configurações do servidor
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Webhook URL - detecta automaticamente baseado no ambiente
    _webhook_url = os.getenv('WEBHOOK_URL', '')
    
    # Se WEBHOOK_URL estiver vazia, tenta inferir do ambiente
    if not _webhook_url:
        # Se for Render (hostname contém 'onrender')
        if 'RENDER' in os.environ or 'onrender' in os.getenv('HOSTNAME', '').lower():
            _webhook_url = 'https://pix-cnpay.onrender.com/webhook'
        else:
            # Para desenvolvimento local
            _webhook_url = os.getenv('WEBHOOK_URL_LOCAL', 'http://localhost:5000/webhook')
    
    WEBHOOK_URL = _webhook_url
    
    # Secret opcional para validar webhooks (comparado com payload.token)
    WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')

config = Config()

# Configurar CORS com origem(s) controladas via variável de ambiente
cors_origins = None
if getattr(config, 'CORS_ORIGINS', None):
    if config.CORS_ORIGINS.strip() == '*' or config.CORS_ORIGINS.strip() == '':
        cors_origins = '*'
    else:
        cors_origins = [o.strip() for o in config.CORS_ORIGINS.split(',') if o.strip()]

if cors_origins:
    CORS(app, resources={r"/api/*": {"origins": cors_origins}})
else:
    CORS(app)

# Validação de configuração crítica
if not config.CNPAY_PUBLIC_KEY or not config.CNPAY_SECRET_KEY:
    logger.error('❌ CNPAY_PUBLIC_KEY e CNPAY_SECRET_KEY não encontradas. Abortando inicialização.')
    raise RuntimeError('Missing CNPAY_PUBLIC_KEY or CNPAY_SECRET_KEY environment variables')

# Log de informações da aplicação
logger.info(f'✅ CNPAY API configurada: {config.CNPAY_API_URL}')
logger.info(f'✅ Webhook URL: {config.WEBHOOK_URL}')
logger.info(f'✅ Porta: {config.PORT}')
logger.info(f'✅ Debug Mode: {config.DEBUG}')

# ==================== HELPERS ====================
def get_cnpay_headers():
    """Retorna os headers necessários para CN Pay API"""
    return {
        'Content-Type': 'application/json',
        'x-public-key': config.CNPAY_PUBLIC_KEY,
        'x-secret-key': config.CNPAY_SECRET_KEY
    }

def generate_identifier():
    """Gera um identificador único para a transação"""
    timestamp = int(datetime.now().timestamp() * 1000)
    import random
    import string
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))
    return f"PIX_{timestamp}_{random_str}"

# ==================== ROTAS - PÁGINAS ====================
@app.route('/')
def index():
    """Página inicial - Checkout"""
    return render_template('checkout.html')

@app.route('/health')
def health():
    """Health check para Render"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'service': 'checkout-pix-cnpay'
    })

# ==================== ROTAS - API ====================
@app.route('/api/create-pix', methods=['POST'])
def create_pix():
    """
    Criar cobrança PIX conforme CN Pay API
    POST /gateway/pix/receive (autenticado)
    Campos obrigatórios: identifier, amount
    """
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({'success': False, 'error': 'Payload JSON inválido'}), 400

        # VALIDAR AMOUNT (obrigatório conforme docs CN Pay)
        amount = data.get('amount')
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            return jsonify({'success': False, 'error': 'Campo "amount" obrigatório e deve ser numérico'}), 400

        if amount <= 0:
            return jsonify({'success': False, 'error': 'Amount deve ser maior que zero'}), 400
        
        # VALIDAR/GERAR IDENTIFIER (obrigatório conforme docs CN Pay)
        identifier = data.get('identifier') or generate_identifier()
        if not identifier or not isinstance(identifier, str) or len(identifier) < 1:
            return jsonify({'success': False, 'error': 'Identifier inválido - deve ser string única'}), 400
        
        # Preparar payload para CN Pay - conforme docs: /gateway/pix/receive
        # Campos obrigatórios: identifier, amount
        payload = {
            'identifier': identifier,
            'amount': float(amount)
        }
        
        # Campos obrigatórios de cliente (CN Pay requer)
        if data.get('client'):
            client = data['client']
            # Validar campos obrigatórios do cliente
            if all(k in client for k in ['name', 'email', 'document', 'phone']):
                payload['client'] = {
                    'name': client.get('name'),
                    'email': client.get('email'),
                    'document': client.get('document'),
                    'phone': client.get('phone')
                }
            else:
                logger.warning(f"Cliente incompleto: {client}")
                payload['client'] = client  # Enviar como está e deixar CN Pay retornar erro
        
        # Campos opcionais de produtos
        if data.get('products'):
            payload['products'] = data['products']
        
        # Campos opcionais de taxas
        if data.get('shippingFee') is not None:
            try:
                payload['shippingFee'] = float(data['shippingFee'])
            except (TypeError, ValueError):
                pass
        
        if data.get('extraFee') is not None:
            try:
                payload['extraFee'] = float(data['extraFee'])
            except (TypeError, ValueError):
                pass
        
        # Adicionar webhook URL se configurada (callbackUrl conforme docs)
        if config.WEBHOOK_URL:
            payload['callbackUrl'] = config.WEBHOOK_URL
        
        logger.info(f"Criando PIX - Valor: R$ {amount} - ID: {identifier}")
        
        # Chamar CN Pay API
        response = requests.post(
            f"{config.CNPAY_API_URL}/gateway/pix/receive",
            json=payload,
            headers=get_cnpay_headers(),
            timeout=30
        )
        
        response_data = response.json()
        
        logger.info(f"Resposta CN Pay (status {response.status_code}): {response_data}")
        
        if response.status_code == 201 or (response.status_code == 200 and response_data.get('status') in ['OK', 'PENDING']):
            logger.info(f"PIX criado com sucesso - Transaction ID: {response_data.get('transactionId')}")
            
            # CN Pay pode retornar pix em diferentes estruturas
            pix_data = response_data.get('pix', {})
            if isinstance(pix_data, str):
                # Se for string, é o código de barras
                pix_data = {'qrCode': pix_data}
            
            # Extrair code (código PIX que o cliente copia)
            pix_code = pix_data.get('code') or response_data.get('code')
            
            # Retornar dados do PIX
            return jsonify({
                'success': True,
                'transactionId': response_data.get('transactionId'),
                'identifier': identifier,
                'status': response_data.get('status'),
                'pix': {
                    'code': pix_code,  # Código PIX para copiar
                    'qrCode': pix_data.get('qrCode') or response_data.get('qrCode') or response_data.get('brCode'),
                    'image': pix_data.get('image') or response_data.get('image'),
                    'base64': pix_data.get('base64') or response_data.get('base64'),
                    'brCode': pix_data.get('brCode') or response_data.get('brCode')
                },
                'order': response_data.get('order', {}),
                'fee': response_data.get('fee', 0),
                'raw_response': response_data  # Debug
            })
        else:
            logger.error(f"Erro ao criar PIX: {response_data}")
            return jsonify({
                'success': False,
                'error': response_data.get('message', 'Erro ao criar PIX'),
                'details': response_data
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição: {str(e)}")
        payload = {'success': False, 'error': 'Erro ao comunicar com CN Pay'}
        if config.DEBUG:
            payload['details'] = str(e)
        return jsonify(payload), 500
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        payload = {'success': False, 'error': 'Erro interno do servidor'}
        if config.DEBUG:
            payload['details'] = str(e)
        return jsonify(payload), 500

@app.route('/api/check-payment/<transaction_id>', methods=['GET'])
def check_payment(transaction_id):
    """
    Verificar status do pagamento conforme CN Pay API
    GET /gateway/transactions?id=<transaction_id>&clientIdentifier=<client_identifier>
    """
    try:
        client_identifier = request.args.get('clientIdentifier')
        
        logger.info(f"📋 Verificando status - Transaction ID: {transaction_id}")
        
        # Preparar parâmetros conforme docs CN Pay
        params = {'id': transaction_id}
        if client_identifier:
            params['clientIdentifier'] = client_identifier
        
        response = requests.get(
            f"{config.CNPAY_API_URL}/gateway/transactions",
            params=params,
            headers=get_cnpay_headers(),
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Transação encontrada - Status: {data.get('status')}")
            
            return jsonify({
                'success': True,
                'transaction': {
                    'id': data.get('id'),
                    'clientIdentifier': data.get('clientIdentifier'),
                    'status': data.get('status'),
                    'amount': data.get('amount'),
                    'paymentMethod': data.get('paymentMethod'),
                    'createdAt': data.get('createdAt'),
                    'payedAt': data.get('payedAt'),
                    'pixInformation': data.get('pixInformation')
                }
            })
        else:
            logger.warning(f"⚠️ Transação não encontrada - ID: {transaction_id}")
            return jsonify({
                'success': False,
                'error': 'Transação não encontrada'
            }), 404
            
    except Exception as e:
        logger.error(f"❌ Erro ao verificar pagamento: {str(e)}")
        payload = {'success': False, 'error': 'Erro interno do servidor'}
        if config.DEBUG:
            payload['details'] = str(e)
        return jsonify(payload), 500

# ==================== WEBHOOK ====================
@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Receber notificações de pagamento da CN Pay
    Validar token conforme documentação CN Pay
    Eventos: TRANSACTION_PAID, TRANSACTION_CREATED, TRANSACTION_CANCELED, TRANSACTION_REFUNDED
    """
    try:
        data = request.get_json(silent=True)
        if not data:
            logger.warning('❌ Webhook: payload vazio ou inválido')
            return jsonify({'success': False, 'error': 'Payload inválido'}), 400

        event = data.get('event')
        token = data.get('token')
        transaction = data.get('transaction', {})
        client = data.get('client', {})
        
        # Validar token do webhook conforme docs CN Pay
        # O token é gerado pelo CN Pay e deve ser validado
        if not token:
            logger.warning('⚠️ Webhook sem token recebido')
        
        # Se WEBHOOK_SECRET configurada (verificação adicional), validar
        if config.WEBHOOK_SECRET:
            if not token or token != config.WEBHOOK_SECRET:
                logger.error('🔐 Webhook token INVÁLIDO - rejeitando requisição')
                return jsonify({'success': False, 'error': 'Invalid webhook token'}), 401
        
        logger.info("=" * 70)
        logger.info(f"📩 Webhook recebido: {event}")
        logger.info("=" * 70)
        logger.info(f"Transaction ID: {transaction.get('id')}")
        logger.info(f"Identifier: {transaction.get('identifier')}")
        logger.info(f"Status: {transaction.get('status')}")
        logger.info(f"Valor: R$ {transaction.get('amount')}")
        logger.info(f"Método: {transaction.get('paymentMethod')}")
        logger.info(f"Cliente: {client.get('name')} - {client.get('email')}")
        logger.info("=" * 70)

        # Processar eventos conforme documentação CN Pay
        if event == 'TRANSACTION_PAID':
            logger.info("💰 PAGAMENTO CONFIRMADO!")
            # Aqui você deve:
            # - Atualizar banco de dados com status PAID
            # - Liberar produto/serviço para o cliente
            # - Enviar email de confirmação
            # - Disparar automações (webhooks internos, etc.)
            
        elif event == 'TRANSACTION_CREATED':
            logger.info("✅ Transação criada na CN Pay")
            # Cobrança foi criada com sucesso
            
        elif event == 'TRANSACTION_CANCELED':
            logger.info("❌ Transação cancelada")
            # Cobrança foi cancelada pelo sistema ou cliente
            
        elif event == 'TRANSACTION_REFUNDED':
            logger.info("↩️ Transação estornada")
            # Pagamento foi reembolsado
            # Aqui você deve:
            # - Revogar acesso ao produto
            # - Atualizar banco de dados
            # - Enviar email de estorno
        
        else:
            logger.warning(f"⚠️ Evento desconhecido: {event}")
        
        # Retornar sucesso (obrigatório para CN Pay não reenviar)
        return jsonify({
            'success': True,
            'message': 'Webhook processado com sucesso'
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Erro ao processar webhook: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== ERRO HANDLERS ====================
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Rota não encontrada'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Erro interno do servidor'}), 500

# ==================== EXECUTAR APLICAÇÃO ====================
if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("🚀 Iniciando servidor...")
    logger.info(f"📡 Porta: {config.PORT}")
    logger.info(f"🔧 Debug: {config.DEBUG}")
    logger.info(f"🔑 CN Pay API: {config.CNPAY_API_URL}")
    if config.WEBHOOK_URL:
        logger.info(f"🔔 Webhook URL: {config.WEBHOOK_URL}")
    logger.info("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=config.PORT,
        debug=config.DEBUG
    )
