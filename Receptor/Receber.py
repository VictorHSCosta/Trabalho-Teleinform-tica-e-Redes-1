# from flask import Flask, render_template, request, jsonify
# from backend.conversores import bits_para_texto
# import socket
# import threading
# import json
# from backend.arrumar_codigo import arrumar_codigo
# import os

# app = Flask(__name__)

# # Configuração do servidor socket
# HOST = '0.0.0.0'  # Permite conexões de qualquer computador na rede
# PORTA = 12345     # Porta do servidor socket

# def servidor_socket():
#     """Servidor TCP que recebe os dados"""
#     servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # Habilita a reutilização de endereço (opcional, mas pode ajudar)
#     servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     servidor.bind((HOST, PORTA))
#     servidor.listen(5)
#     print(f"Servidor TCP rodando em {HOST}:{PORTA}")

#     while True:
#         conexao, endereco = servidor.accept()
#         print(f"Conexão estabelecida com: {endereco}")
#         print("Recebendo dados...")

#         try:
#             # Recebe os dados e converte de JSON
#             dados_recebidos = conexao.recv(4096).decode()
#             dados = json.loads(dados_recebidos)
#             sinal_modulado = dados["sinal_modulado"]
#             enquadramento = dados["metodo_enquadramento"]
#             tipo_modulacao = dados["tipo_modulacao"]
#             deteccao_erro = dados["deteccao_erro"]

#             # Exibe os dados recebidos
#             print(f"Sinal modulado: {sinal_modulado}")
#             print(f"Enquadramento: {enquadramento}")
#             print(f"Tipo de modulação: {tipo_modulacao}")
#             print(f"Detecção de erro: {deteccao_erro}")

#             # Corrigir ou não os quadros
#             try:    
#                 resposta = arrumar_codigo(sinal_modulado, enquadramento, deteccao_erro)
#             except Exception as e:
#                 conexao.sendall(json.dumps({"erro": f"Erro ao arrumar código: {e}"}).encode())
#                 continue

#             # Prepara os dados para enviar de volta ao cliente
#             dados_enviar = {
#                 "texto": resposta[0],
#                 "bits": resposta[1],
#                 "correcao": deteccao_erro,
#                 "enquadramento": enquadramento,
#                 "modulacao": tipo_modulacao
#             }

#              # Emite o evento 'atualizacao' para todos os clientes conectados
#              # Emite o evento 'atualizacao' para todos os clientes conectados
            
            
           
#             try:
#                 if len(resposta[1]) > 0:
#                     texto = bits_para_texto(resposta[1])
#                 else:
#                     texto = resposta[0]
#             except ValueError as e:
#                 conexao.sendall(json.dumps({"erro": f"Erro na conversão para texto: {e}"}).encode())
#                 continue

#             # Envia a resposta para o cliente
#             resposta_json = json.dumps({"texto_recebido": texto})
#             conexao.sendall(resposta_json.encode())

#             print(f"Texto recebido: {texto}")
        
#         except Exception as e:
#             conexao.sendall(json.dumps({"erro": f"Erro inesperado: {str(e)}"}).encode())

#         conexao.close()

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     # Verifica se está no processo filho do reloader
#     if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
#         thread_socket = threading.Thread(target=servidor_socket, daemon=True)
#         thread_socket.start()

#     app.run(debug=True, host='0.0.0.0', port=3000)


from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from backend.conversores import bits_para_texto
import socket
import threading
import json
from backend.arrumar_codigo import arrumar_codigo
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minha_chave_secreta'  # defina uma chave secreta
socketio = SocketIO(app)

# Configuração do servidor socket TCP
HOST = '0.0.0.0'  # Permite conexões de qualquer computador na rede
PORTA = 12345     # Porta do servidor socket

def servidor_socket():
    """Servidor TCP que recebe os dados e emite o evento 'atualizacao' via SocketIO."""
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(5)
    print(f"Servidor TCP rodando em {HOST}:{PORTA}")

    while True:
        conexao, endereco = servidor.accept()
        print(f"Conexão estabelecida com: {endereco}")
        print("Recebendo dados...")

        try:
            # Recebe os dados e converte de JSON
            dados_recebidos = conexao.recv(4096).decode()
            dados = json.loads(dados_recebidos)
            sinal_modulado = dados["sinal_modulado"]
            enquadramento = dados["metodo_enquadramento"]
            tipo_modulacao = dados["tipo_modulacao"]
            deteccao_erro = dados["deteccao_erro"]

            print(f"Sinal modulado: {sinal_modulado}")
            print(f"Enquadramento: {enquadramento}")
            print(f"Tipo de modulação: {tipo_modulacao}")
            print(f"Detecção de erro: {deteccao_erro}")

            # Processa os dados (corrige ou não os quadros)
            try:
                resposta = arrumar_codigo(sinal_modulado, enquadramento, deteccao_erro)
            except Exception as e:
                conexao.sendall(json.dumps({"erro": f"Erro ao arrumar código: {e}"}).encode())
                continue

            # Prepara os dados que serão enviados para o front-end
            dados_enviar = {
                "texto": resposta[0],
                "bits": resposta[1],
                "correcao": deteccao_erro,
                "enquadramento": enquadramento,
                "modulacao": tipo_modulacao
            }

            # Emite o evento 'atualizacao' para os clientes conectados via SocketIO
            socketio.emit('atualizacao', dados_enviar)
            print("Evento 'atualizacao' emitido:", dados_enviar)

            try:
                if len(resposta[1]) > 0:
                    texto = bits_para_texto(resposta[1])
                else:
                    texto = resposta[0]
            except ValueError as e:
                conexao.sendall(json.dumps({"erro": f"Erro na conversão para texto: {e}"}).encode())
                continue

            # Envia a resposta ao cliente que enviou os dados via socket TCP
            resposta_json = json.dumps({"texto_recebido": texto})
            conexao.sendall(resposta_json.encode())
            print(f"Texto recebido: {texto}")

        except Exception as e:
            conexao.sendall(json.dumps({"erro": f"Erro inesperado: {str(e)}"}).encode())

        conexao.close()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Inicia a thread do servidor TCP apenas quando o reloader já tiver iniciado
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        thread_socket = threading.Thread(target=servidor_socket, daemon=True)
        thread_socket.start()

    # Utilize socketio.run para iniciar o servidor Flask com suporte a WebSocket
    socketio.run(app, debug=True, host='0.0.0.0', port=3000)
