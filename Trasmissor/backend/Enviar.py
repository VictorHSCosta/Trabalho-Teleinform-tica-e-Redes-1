import socket
import json
from .deteccao_de_erros import adicionar_paridade, verificar_paridade, adicionar_crc32, verificar_crc32
from .adicionar_erro import adicionar_erro
from .conversores import texto_para_bits
from .hamming import aplicar_hamming_quadros
from .modulador import modular_quadros
from .enquadramento import enquadramento_contagem_caracteres, enquadramento_insercao_bytes

def enviar_dados(HOST, PORTA, texto, tipo_modulacao, porcentagem_erro, enquadramento, deteccao_erro):
    """
    Conecta-se ao servidor, processa a mensagem e a envia via socket TCP.
    """
    try:
        # Criar socket
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.settimeout(5)  # Definir timeout de 5 segundos
        print(f"📡 Tentando conectar ao servidor {HOST}:{PORTA}...")
        cliente.connect((HOST, PORTA))
        print(f"✅ Conectado ao servidor {HOST}:{PORTA}")

        # 🔹 1️⃣ Conversão do Texto para Bits
        bits = texto_para_bits(texto)
        bits_com_erro = adicionar_erro(bits, porcentagem_erro)
        print(f"🔹 Bits após adição de erro: {bits_com_erro}")

        # 🔹 2️⃣ Enquadramento
        if enquadramento == "Contagem de Caracteres":
            quadros = enquadramento_contagem_caracteres(bits_com_erro)
        elif enquadramento == "Inserção de Bytes":
            quadros = enquadramento_insercao_bytes(bits_com_erro)
        else:
            print("❌ Método de enquadramento inválido!")
            return

        # 🔹 3️⃣ Aplicação do Código de Hamming
        quadros_hamming = aplicar_hamming_quadros(quadros)

        # 🔹 4️⃣ Aplicação da Detecção de Erros
        if deteccao_erro == "Bit de Paridade":
            quadros_checagem = [adicionar_paridade(quadro) for quadro in quadros_hamming]
        elif deteccao_erro == "CRC":
            quadros_checagem = [adicionar_crc32(quadro) for quadro in quadros_hamming]
        else:
            print("❌ Método de detecção inválido!")
            return

        # 🔹 5️⃣ Modulação
        sinais_modulados = modular_quadros(quadros_checagem, tipo_modulacao)

        # 🔹 6️⃣ Preparação e envio dos dados
        dados = {
            "sinal_modulado": sinais_modulados,
            "metodo_enquadramento": enquadramento,
            "tipo_modulacao": tipo_modulacao,
            "deteccao_erro": deteccao_erro,
        }

        print(f"📡 Dados sendo enviados: {json.dumps(dados, indent=4)}")
        cliente.sendall(json.dumps(dados).encode())
        print("✅ Dados enviados com sucesso!")

        # 🔹 7️⃣ Receber Resposta do Servidor
        resposta = cliente.recv(4096).decode()
        resposta_json = json.loads(resposta)

        if "texto_recebido" in resposta_json:
            print(f"✅ Texto decodificado recebido: {resposta_json['texto_recebido']}")
        else:
            print(f"❌ Erro no servidor: {resposta_json['erro']}")

    except socket.error as e:
        print(f"❌ Erro de conexão: {e}")

    finally:
        cliente.close()

if __name__ == "__main__":
    enviar_dados(
        HOST="127.0.0.1",
        PORTA=12345,
        texto="Hello, World! 😊",
        tipo_modulacao="NRZ",
        porcentagem_erro=10,
        enquadramento="Contagem de Caracteres",
        deteccao_erro="Bit de Paridade"
    )
