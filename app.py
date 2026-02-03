"""
Aplicação Flask - Checkout PIX CN Pay
Deploy: Render.com
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
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
    
    # Webhook URL (será a URL do Render + /webhook)
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
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
    if config.DEBUG:
        logger.warning('CNPAY keys not set — usando chaves de exemplo em DEBUG. Não use em produção.')
        # chaves exemplo somente para testes locais
        config.CNPAY_PUBLIC_KEY = config.CNPAY_PUBLIC_KEY or 'financeiro_moqjrint4j9xhzzt'
        config.CNPAY_SECRET_KEY = config.CNPAY_SECRET_KEY or 'c3qfmxlk7iw147u7g5b47l2u7eghbd6vi3sgsb908afhrcvh2tqsksoxi7zyr75e'
    else:
        logger.error('CNPAY_PUBLIC_KEY e CNPAY_SECRET_KEY não encontradas. Abortando inicialização.')
        raise RuntimeError('Missing CNPAY_PUBLIC_KEY or CNPAY_SECRET_KEY environment variables')

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
    Criar cobrança PIX
    Body: { "amount": 25.00, "client": {...}, "products": [...] }
    """
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({'success': False, 'error': 'Payload JSON inválido'}), 400

        # Validar dados
        amount = data.get('amount')
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            return jsonify({'success': False, 'error': 'Valor inválido'}), 400

        if amount <= 0:
            return jsonify({'success': False, 'error': 'Valor inválido'}), 400
        
        # Gerar identificador único
        identifier = generate_identifier()
        
        # Preparar payload para CN Pay
        payload = {
            'identifier': identifier,
            'amount': float(amount),
            'client': data.get('client', {
                'name': 'Cliente',
                'email': 'cliente@exemplo.com',
                'phone': '11999999999'
            }),
            'products': data.get('products', [{
                'name': 'Pushin Pay - Kivora',
                'price': float(amount),
                'quantity': 1
            }])
        }
        
        # Adicionar webhook URL se configurada
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
        
        if response.status_code == 201 and response_data.get('status') in ['OK', 'PENDING']:
            logger.info(f"PIX criado com sucesso - Transaction ID: {response_data.get('transactionId')}")
            
            # Retornar dados do PIX
            return jsonify({
                'success': True,
                'transactionId': response_data.get('transactionId'),
                'identifier': identifier,
                'status': response_data.get('status'),
                'pix': {
                    'qrCode': response_data.get('pix', {}).get('qrCode'),
                    'image': response_data.get('pix', {}).get('image'),
                    'base64': response_data.get('pix', {}).get('base64')
                },
                'order': response_data.get('order', {}),
                'fee': response_data.get('fee', 0)
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
    Verificar status do pagamento
    """
    try:
        logger.info(f"Verificando status - Transaction ID: {transaction_id}")
        
        response = requests.get(
            f"{config.CNPAY_API_URL}/gateway/transactions",
            params={'id': transaction_id},
            headers=get_cnpay_headers(),
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                'success': True,
                'transaction': {
                    'id': data.get('id'),
                    'status': data.get('status'),
                    'amount': data.get('amount'),
                    'paymentMethod': data.get('paymentMethod'),
                    'createdAt': data.get('createdAt'),
                    'payedAt': data.get('payedAt'),
                    'pixInformation': data.get('pixInformation')
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Transação não encontrada'
            }), 404
            
    except Exception as e:
        logger.error(f"Erro ao verificar pagamento: {str(e)}")
        payload = {'success': False, 'error': 'Erro interno do servidor'}
        if config.DEBUG:
            payload['details'] = str(e)
        return jsonify(payload), 500

# ==================== WEBHOOK ====================
@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Receber notificações de pagamento da CN Pay
    """
    try:
        data = request.get_json(silent=True)
        if not data:
            logger.warning('Webhook: payload vazio ou inválido')
            return jsonify({'success': False, 'error': 'Payload inválido'}), 400

        event = data.get('event')
        token = data.get('token')
        transaction = data.get('transaction', {})
        client = data.get('client', {})
        
        logger.info("=" * 60)
        logger.info(f"📩 Webhook recebido: {event}")
        logger.info("=" * 60)
        logger.info(f"Token: {'<redacted>' if token else '(none)'}")
        logger.info(f"Transaction ID: {transaction.get('id')}")
        logger.info(f"Status: {transaction.get('status')}")
        logger.info(f"Valor: R$ {transaction.get('amount')}")
        logger.info(f"Cliente: {client.get('name')} - {client.get('email')}")
        logger.info("=" * 60)

        # Validar token do webhook quando configurado
        if config.WEBHOOK_SECRET:
            if not token or token != config.WEBHOOK_SECRET:
                logger.warning('Webhook token inválido')
                return jsonify({'success': False, 'error': 'Invalid webhook token'}), 401
        
        # Processar eventos
        if event == 'TRANSACTION_PAID':
            logger.info("💰 PAGAMENTO CONFIRMADO!")
            # Aqui você deve:
            # - Atualizar banco de dados
            # - Liberar produto/serviço
            # - Enviar email de confirmação
            # - Disparar automações
            
        elif event == 'TRANSACTION_CREATED':
            logger.info("✅ Transação criada")
            
        elif event == 'TRANSACTION_CANCELED':
            logger.info("❌ Transação cancelada")
            
        elif event == 'TRANSACTION_REFUNDED':
            logger.info("↩️ Transação estornada")
            # Aqui você deve:
            # - Revogar acesso ao produto
            # - Atualizar banco de dados
            # - Enviar email de estorno
        
        # Retornar sucesso (obrigatório)
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
