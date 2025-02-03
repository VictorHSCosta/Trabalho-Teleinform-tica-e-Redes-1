from flask import Flask, render_template, request, jsonify
from backend.conversores import bits_para_texto
import socket
import threading
import json
from backend.arrumar_codigo import arrumar_codigo

app = Flask(__name__)

# Configuração do servidor socket
HOST = '0.0.0.0'  # Permite conexões de qualquer computador na rede
PORTA = 12345  # Porta do servidor socket

texto = ""

def servidor_socket():
    """Servidor TCP que recebe os dados do transmissor"""
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reutilizar a porta imediatamente
    servidor.bind((HOST, PORTA))
    servidor.listen(5)
    print(f"📡 Servidor TCP rodando em {HOST}:{PORTA}, aguardando conexão...")

    while True:
        conexao, endereco = servidor.accept()
        print(f"\n🔹 Conexão estabelecida com: {endereco}")
        print("📩 Recebendo dados...")

        try:
            # Recebe os dados e converte de JSON
            buffer = []  # Corrigido erro de sintaxe
            while True:
                parte = conexao.recv(4096)
                if not parte:
                    break
                buffer.append(parte)
            dados_recebidos = b''.join(buffer).decode()
            
            if not dados_recebidos:
                print("❌ Nenhum dado recebido.")
                conexao.close()
                continue

            dados = json.loads(dados_recebidos)
            
            # Extraindo os dados recebidos
            sinal_modulado = dados.get("sinal_modulado", [])
            enquadramento = dados.get("metodo_enquadramento", "")
            tipo_modulacao = dados.get("tipo_modulacao", "")
            deteccao_erro = dados.get("deteccao_erro", "")

            # Printando os dados recebidos para conferência
            print(f"🔹 Sinal modulado recebido ({tipo_modulacao}): {sinal_modulado}")
            print(f"🔹 Método de enquadramento: {enquadramento}")
            print(f"🔹 Método de detecção de erro: {deteccao_erro}")

            if not sinal_modulado:
                conexao.sendall(json.dumps({"erro": "Sinal modulado inválido ou vazio."}).encode())
                conexao.close()
                continue

            # 🔹 Corrigir ou não os quadros
            try:
                resposta = arrumar_codigo(sinal_modulado, enquadramento, deteccao_erro)
            except Exception as e:
                erro_msg = f"Erro ao processar código: {e}"
                print(f"❌ {erro_msg}")
                conexao.sendall(json.dumps({"erro": erro_msg}).encode())
                continue

            # 🔹 Converter bits para texto, se possível
            try:
                if len(resposta[1]) > 0:
                    texto = bits_para_texto(resposta[1])
                else:
                    texto = resposta[0]
            except ValueError as e:
                erro_msg = f"Erro na conversão de bits para texto: {e}"
                print(f"❌ {erro_msg}")
                conexao.sendall(json.dumps({"erro": erro_msg}).encode())
                continue

            # 🔹 Enviar resposta para o transmissor
            resposta_json = json.dumps({"texto_recebido": texto})
            conexao.sendall(resposta_json.encode())

            print(f"📜 Texto decodificado e enviado: {texto}")

        except json.JSONDecodeError:
            erro_msg = "❌ Erro ao decodificar JSON recebido."
            print(erro_msg)
            conexao.sendall(json.dumps({"erro": erro_msg}).encode())

        except Exception as e:
            erro_msg = f"❌ Erro inesperado: {str(e)}"
            print(erro_msg)
            conexao.sendall(json.dumps({"erro": erro_msg}).encode())

        finally:
            conexao.close()
            print("🔻 Conexão encerrada.\n")

# Criar uma thread para rodar o servidor socket em paralelo com Flask
thread_socket = threading.Thread(target=servidor_socket, daemon=True)
thread_socket.start()

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
