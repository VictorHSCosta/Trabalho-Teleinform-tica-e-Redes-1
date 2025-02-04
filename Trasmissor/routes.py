import io
import sys
from flask import Flask, render_template, request, jsonify
import socket
from backend.bytecode import get_bytecode
from dotenv import load_dotenv
import os
from backend.Enviar import enviar_dados
from backend.enquadramento import enquadramento_insercao_bytes

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/home")
def about():
    return render_template("home.html")

@app.route("/verificar_ip", methods=["POST"])
def verificar_ip():
    data = request.json
    ip = data.get("ip")
    
    load_dotenv()

    ip = data.get("ip")
    if ip:
        with open('.env', 'a') as env_file:
            env_file.write(f"\nDEFAULT_IP={ip}")
    
    if not ip:
        return jsonify({"erro": "IP inválido!"}), 400

    try:
        # Testar a conexão com o servidor Flask usando socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # Tempo limite para conexão
        sock.connect((ip, 12345))
        sock.close()
        return jsonify({"sucesso": True, "mensagem": "IP válido! Redirecionando..."})
    
    except socket.error:
        return jsonify({"erro": "Não foi possível conectar ao IP informado."}), 400
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_bits', methods=['GET'])
def get_bits():
    text = request.args.get('text')  # Obtém o texto da query string
    if not text:
        return jsonify({"bits_array": "Texto não encontrado."}),400
    
    bits_array = get_bytecode(text)
    return jsonify({"bits_array": bits_array})

@app.route("/processar_dados", methods=["POST"])
def processar_dados():
    try:
        # Recebe os dados enviados pelo frontend
        data = request.get_json()

        texto = data.get("text", "")
        tipo_modulacao = data.get("modo", "")
        porcentagem_erro = float(data.get("erro", 0))
        enquadramento = data.get("enquadramento", "")   
        deteccao_erro = data.get("deteccao", "")

        host = os.getenv("DEFAULT_IP")

        # 🛑 Verificação de erro
        if not texto:
            return jsonify({"erro": "Texto não pode ser vazio!"}), 400
        if not host:
            return jsonify({"erro": "O IP do servidor não está definido!"}), 400
        if not tipo_modulacao:
            return jsonify({"erro": "O tipo de modulação não pode ser vazio!"}), 400
        if( porcentagem_erro < 0 or porcentagem_erro > 100):
            return jsonify({"erro": "Porcentagem de erro inválida!"}), 400

        # 🛑 Debug: Printando os dados recebidos
        print("Recebendo dados para processamento:")
        print(f"Texto: {texto}")
        print(f"Modulação: {tipo_modulacao}")
        print(f"Erro: {porcentagem_erro}%")
        print(f"Enquadramento: {enquadramento}")
        print(f"Detecção de erro: {deteccao_erro}")
        
        # 🔹 Redireciona a saída do print() para capturar a saída do script
        host = os.getenv("DEFAULT_IP")

        # 🔹 Redireciona a saída do print() para capturar a saída do script
        sys.stdout = io.StringIO()

        # 🔹 Chama `enviar_dados()` com os parâmetros corretos
        
        
        enviar_dados(host, texto, tipo_modulacao, porcentagem_erro, enquadramento, deteccao_erro)
        
        # 🔹 Captura a saída do print()
        resultado = sys.stdout.getvalue()

        # 🔹 Restaura a saída padrão
        sys.stdout = sys.__stdout__

        return jsonify({"resultado": resultado})

    except Exception as e:
        print("🛑 ERRO NO SERVIDOR:", str(e))  # Mostra o erro no terminal
        return jsonify({"erro no servidor": str(e)}), 500
    


if __name__ == "__main__":
    app.run(debug=True)
