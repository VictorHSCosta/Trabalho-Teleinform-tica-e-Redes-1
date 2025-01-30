from flask import Flask, render_template, request, jsonify
from backend.conversores import bits_para_texto
from backend.hamming import hamming_decode
from backend.demodulador import demodular_nrz, demodular_manchester, demodular_bipolar
import socket
import threading
import json

class Config:
    text = ""
    TremDebits = ""
    TremDebitsCorrigido = ""
    HouveErro = False
    MetodoEscolhido = ""
    BitErrado = 0


app = Flask(__name__)

# Configuração do servidor socket
HOST = '0.0.0.0'  # Permite conexões de qualquer computador na rede
PORTA = 12345  # Porta do servidor socket

def servidor_socket():
    """Servidor TCP que recebe os dados"""
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORTA))
    servidor.listen(5)
    print(f"Servidor TCP rodando em {HOST}:{PORTA}")

    while True:
        conexao, endereco = servidor.accept()
        print(f"Conexão estabelecida com: {endereco}")

        try:
            # Recebe os dados e converte de JSON
            dados_recebidos = conexao.recv(4096).decode()
            dados = json.loads(dados_recebidos)
            sinal_modulado = dados["sinal_modulado"]
            tipo_modulacao = dados["tipo_modulacao"].lower()

            # Demodulação
            print(f"Demodulando sinal modulado com {tipo_modulacao}...")
            if tipo_modulacao == "nrz":
                bits_demodulados = demodular_nrz(sinal_modulado)
            elif tipo_modulacao == "manchester":
                bits_demodulados = demodular_manchester(sinal_modulado)
            elif tipo_modulacao == "bipolar":
                bits_demodulados = demodular_bipolar(sinal_modulado)
            else:
                conexao.sendall(json.dumps({"erro": "Modulação inválida"}).encode())
                continue

            # Correção de erros
            bits_corrigidos = hamming_decode(''.join(map(str, bits_demodulados)))

            # Conversão para texto
            try:
                texto_recebido = bits_para_texto(list(map(int, bits_corrigidos)))
            except ValueError as e:
                conexao.sendall(json.dumps({"erro": f"Erro na conversão para texto: {e}"}).encode())
                continue

            # Enviar resposta para o cliente
            resposta = json.dumps({"texto_recebido": texto_recebido})
            conexao.sendall(resposta.encode())

            print(f"Texto recebido: {texto_recebido}")
        
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
