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
    """Servidor TCP que recebe os dados"""
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            tipo_modulacao =dados["tipo_modulacao"]
            deteccao_erro = dados["deteccao_erro"]

            #printar tudo que recebeu
            print(f"Sinal modulado: {sinal_modulado}")
            print(f"Enquadramento: {enquadramento}")
            print(f"Tipo de modulação: {tipo_modulacao}")
            print(f"Deteccao de erro: {deteccao_erro}")

            # corrigir ou nao os quadros
            resposta = []

            try:    
                resposta = arrumar_codigo(sinal_modulado, enquadramento, deteccao_erro)
            except Exception as e:
                conexao.sendall(json.dumps({"erro": f"Erro ao arrumar código: {e}"}).encode())
                continue
           
            try:
                if len(resposta[1]) > 0:
                    texto = bits_para_texto(resposta[1])
                else:
                    texto = resposta[0]
            except ValueError as e:
                conexao.sendall(json.dumps({"erro": f"Erro na conversão para texto: {e}"}).encode())
                continue

            # Enviar resposta para o cliente
            resposta = json.dumps({"texto_recebido": texto})
            conexao.sendall(resposta.encode())

            print(f"Texto recebido: {texto}")
        
        except Exception as e:
            conexao.sendall(json.dumps({"erro": f"Erro inesperado: {str(e)}"}).encode())

        conexao.close()

# Criar uma thread para rodar o servidor socket em paralelo com Flask
thread_socket = threading.Thread(target=servidor_socket, daemon=True)
thread_socket.start()

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
