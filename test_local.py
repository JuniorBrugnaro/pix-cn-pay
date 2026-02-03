#!/usr/bin/env python3
"""
Script para testar a aplicação localmente antes do deploy
"""

import subprocess
import sys
import os

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    print_header("Verificando Python")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        print(f"   Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]}")
    return True

def check_files():
    """Verifica se todos os arquivos necessários existem"""
    print_header("Verificando Arquivos")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'Procfile',
        'templates/checkout.html'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} não encontrado")
            all_exist = False
    
    return all_exist

def install_dependencies():
    """Instala as dependências"""
    print_header("Instalando Dependências")
    
    try:
        subprocess.check_call([
            sys.executable, 
            '-m', 
            'pip', 
            'install', 
            '-r', 
            'requirements.txt'
        ])
        print("\n✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Erro ao instalar dependências")
        return False

def check_env_file():
    """Verifica se o arquivo .env existe"""
    print_header("Verificando Variáveis de Ambiente")
    
    if os.path.exists('.env'):
        print("✅ Arquivo .env encontrado")
        print("\n📝 Conteúdo do .env:")
        with open('.env', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key = line.split('=')[0]
                    print(f"   • {key}")
        return True
    else:
        print("⚠️  Arquivo .env não encontrado")
        print("   Usando valores padrão do código")
        return True

def run_tests():
    """Executa testes básicos"""
    print_header("Executando Testes")
    
    try:
        # Importar a aplicação
        import app as flask_app
        print("✅ app.py importado com sucesso")
        
        # Verificar rotas
        routes = []
        for rule in flask_app.app.url_map.iter_rules():
            routes.append(f"{rule.endpoint}: {rule.rule}")
        
        print(f"\n📡 Rotas encontradas ({len(routes)}):")
        for route in sorted(routes):
            print(f"   • {route}")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao importar aplicação: {e}")
        return False

def start_server():
    """Inicia o servidor Flask"""
    print_header("Iniciando Servidor")
    
    print("🚀 Servidor Flask iniciando...")
    print("📍 URL: http://localhost:5000")
    print("\n⚠️  Pressione Ctrl+C para parar o servidor\n")
    print("=" * 60 + "\n")
    
    try:
        import app as flask_app
        flask_app.app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Servidor parado")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")

def main():
    """Função principal"""
    print("\n" + "=" * 60)
    print("  🧪 TESTE LOCAL - CHECKOUT PIX CN PAY")
    print("=" * 60)
    
    # Verificações
    checks = [
        ("Python", check_python_version),
        ("Arquivos", check_files),
        ("Variáveis de Ambiente", check_env_file),
    ]
    
    for name, check_func in checks:
        if not check_func():
            print(f"\n❌ Falha na verificação: {name}")
            print("   Corrija os erros antes de continuar")
            sys.exit(1)
    
    # Perguntar se deseja instalar dependências
    print("\n" + "=" * 60)
    response = input("Deseja instalar as dependências? (s/n): ").lower()
    if response == 's':
        if not install_dependencies():
            sys.exit(1)
    
    # Executar testes
    if not run_tests():
        print("\n❌ Testes falharam")
        sys.exit(1)
    
    # Perguntar se deseja iniciar servidor
    print("\n" + "=" * 60)
    response = input("\nDeseja iniciar o servidor agora? (s/n): ").lower()
    if response == 's':
        start_server()
    else:
        print("\n✅ Tudo pronto!")
        print("\nPara iniciar o servidor manualmente, execute:")
        print("   python app.py")
        print("\nOu:")
        print("   python test_local.py")

if __name__ == '__main__':
    main()
