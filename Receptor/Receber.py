import socket
import json
import threading
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from backend.deteccao_de_erros import verificar_paridade, verificar_crc32
from backend.conversores import bits_para_texto
from backend.hamming import corrigir_erros_quadros
from backend.demodulador import demodular_sinal 
from backend.enquadramento import desenquadramento_contagem_caracteres, desenquadramento_insercao_bytes

app = Flask(__name__)
CORS(app)

# 🔹 Variável Global para armazenar últimos dados recebidos
ultimo_dado = {
    "texto": "Nenhum dado recebido ainda",
    "bits": "Aguardando...",
    "correcao": "Aguardando...",
    "enquadramento": "Aguardando...",
    "modulacao": "Aguardando..."
}

# 🔹 Configuração do Servidor TCP
HOST = "0.0.0.0"
PORTA = 12345

def processar_mensagem(dados):
    """
    Processa a mensagem recebida do transmissor, incluindo:
     Demodulação
     Desenquadramento
     Verificação e correção de erros
     Conversão final para texto
    """

    try:
        print(f"🔍 Dados recebidos: {dados}")

        # 🔹 Extraindo informações do JSON
        sinais_modulados = dados["sinal_modulado"]
        enquadramento = dados["metodo_enquadramento"]
        tipo_modulacao = dados["tipo_modulacao"]
        deteccao_erro = dados["deteccao_erro"]

        print(f"🔹 Modulação usada: {tipo_modulacao}")
        print(f"🔹 Método de enquadramento: {enquadramento}")
        print(f"🔹 Método de detecção de erro: {deteccao_erro}")

        # 🔹 1️⃣ Demodulação (Agora chamando corretamente `demodular_sinal`)
        print("📡 Demodulando sinal...")
        quadros_demodulados = demodular_sinal(sinais_modulados, tipo_modulacao)
        print(f"🔍 Quadros demodulados: {quadros_demodulados}")

        # 🔹 2️⃣ Desenquadramento (logo após a demodulação)
        print("📡 Desenquadrando quadros...")
        if enquadramento == "Contagem de Caracteres":
            quadros_desenquadrados = desenquadramento_contagem_caracteres(quadros_demodulados)
        elif enquadramento == "Inserção de Bytes":
            quadros_desenquadrados = desenquadramento_insercao_bytes(quadros_demodulados)
        else:
            return "❌ Erro: Método de enquadramento desconhecido."

        print(f"📡 Bits após desenquadramento: {quadros_desenquadrados}")

        # 🔹 3️⃣ Verificação de Erros (Bit de Paridade ou CRC)
        erro_detectado = False
        if deteccao_erro == "Bit de Paridade":
            erro_detectado = not verificar_paridade(quadros_desenquadrados)
        elif deteccao_erro == "CRC":
            erro_detectado = not verificar_crc32(quadros_desenquadrados)

        print(f"⚠ Erro detectado? {erro_detectado}")

        # 🔹 4️⃣ Correção de Erros com Hamming (após detecção)
        print("🔍 Tentando corrigir erros usando Hamming...")
        quadros_corrigidos = corrigir_erros_quadros(quadros_desenquadrados)
        print(f"✅ Quadros corrigidos: {quadros_corrigidos}")

        # 🔹 5️⃣ Conversão de Bits para Texto
        mensagem_final = bits_para_texto(quadros_corrigidos)
        print(f"✅ Mensagem decodificada: {mensagem_final}")

        return mensagem_final

    except Exception as e:
        print(f"❌ Erro ao processar mensagem: {e}")
        return f"Erro ao processar mensagem: {e}"


def servidor_socket():
    """Servidor TCP que recebe os dados."""
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(5)
    print(f"📡 Servidor TCP rodando em {HOST}:{PORTA}")

    while True:
        conexao, endereco = servidor.accept()
        print(f"🔹 Conexão estabelecida com: {endereco}")

        try:
            dados_recebidos = conexao.recv(4096).decode()
            print(f"🔍 String recebida (antes de processar JSON): '{dados_recebidos}'")
            if not dados_recebidos:
                print("❌ Nenhum dado recebido!")
                continue

            dados = json.loads(dados_recebidos)
            mensagem_decodificada = processar_mensagem(dados)

            # 🔹 Armazenar dados recebidos
            global ultimo_dado
            ultimo_dado.update({
                "texto": mensagem_decodificada,
                "bits": dados["sinal_modulado"],
                "correcao": dados["deteccao_erro"],
                "enquadramento": dados["metodo_enquadramento"],
                "modulacao": dados["tipo_modulacao"]
            })

            resposta_json = json.dumps({"texto_recebido": mensagem_decodificada})
            conexao.sendall(resposta_json.encode())

        except Exception as e:
            print(f"❌ Erro ao processar dados: {e}")
            conexao.sendall(json.dumps({"erro": str(e)}).encode())

        finally:
            conexao.close()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dados')
def obter_dados():
    return jsonify(ultimo_dado)

if __name__ == '__main__':
    threading.Thread(target=servidor_socket, daemon=True).start()
    app.run(debug=True, host='0.0.0.0', port=3000)
