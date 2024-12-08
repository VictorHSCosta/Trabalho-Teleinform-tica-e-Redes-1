import os
from dotenv import load_dotenv, set_key

env_file = ".env"

if not os.path.exists(env_file):
    open(env_file, "w").close()

# Identificar o diretório raiz do projeto (onde o script está sendo executado)
diretorio_raiz = os.path.abspath(os.path.dirname(__file__))

# Salvar o diretório raiz no arquivo .env
load_dotenv(env_file)  # Carregar variáveis existentes no .env
set_key(env_file, "DIRETORIO_RAIZ", diretorio_raiz)

# Mensagem de confirmação
print(f"Diretório raiz identificado e salvo no .env:")
print(f"DIRETORIO_RAIZ={diretorio_raiz}")

DIRETORIO_RAIZ = os.getenv("DIRETORIO_RAIZ")

def get_path():
    return DIRETORIO_RAIZ
