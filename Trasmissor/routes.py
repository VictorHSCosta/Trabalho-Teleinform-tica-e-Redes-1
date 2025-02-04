from flask import Flask, render_template, request, jsonify
import socket
import os
from backend.Enviar import enviar_dados
from dotenv import load_dotenv

app = Flask(__name__)

# 🔹 Carregar variáveis de ambiente
load_dotenv()

@app.route("/")
def index():
    """Renderiza a página inicial"""
    return render_template("index.html")

@app.route("/home")
def home():
    """Renderiza a página inicial após verificação"""
    return render_template("home.html")

@app.route("/verificar_ip", methods=["POST"])
def verificar_ip():
    """
    Verifica se o IP fornecido é válido e salva no `.env`.
    Testa conexão com o servidor receptor para garantir que está online.
    """
    data = request.json
    ip = data.get("ip")

    if not ip:
        return jsonify({"erro": "IP inválido!"}), 400

    try:
        # 🔹 Testa conexão com o receptor via socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # Tempo limite de resposta
        sock.connect((ip, 12345))  # Porta fixa 12345
        sock.close()

        # 🔹 Salva o IP no `.env`
        with open(".env", "w") as env_file:
            env_file.write(f"DEFAULT_IP={ip}\n")

        return jsonify({"sucesso": True, "mensagem": "IP válido! Conexão estabelecida."})

    except socket.error:
        return jsonify({"erro": "Não foi possível conectar ao IP informado. Verifique se o receptor está rodando."}), 400

@app.route("/get_bits", methods=["GET"])
def get_bits():
    """Converte texto em bits"""
    text = request.args.get("text")
    if not text:
        return jsonify({"bits_array": "Texto não encontrado."}), 400
    
    from backend.conversores import texto_para_bits
    bits_array = texto_para_bits(text)
    return jsonify({"bits_array": bits_array})

@app.route("/processar_dados", methods=["POST"])
def processar_dados():
    """
    Recebe os dados do frontend e inicia o processo de envio ao receptor.
    Inclui:
    - Conversão de texto para bits
    - Modulação
    - Enquadramento
    - Inserção de erro
    - Envio via socket para o receptor
    """

    try:
        # 🔹 Recebe os dados do frontend
        data = request.get_json()

        texto = data.get("text", "").strip()
        tipo_modulacao = data.get("modo", "").strip()
        porcentagem_erro = float(data.get("erro", 0))
        enquadramento = data.get("enquadramento", "").strip()
        deteccao_erro = data.get("deteccao", "").strip()

        # 🔹 Obtém o IP do receptor salvo no `.env`
        host = os.getenv("DEFAULT_IP")
        port = 12345  # Definição explícita da porta do receptor

        if not host:
            return jsonify({"erro": "O IP do servidor receptor não está definido!"}), 400

        # 🛑 Verificação de erros
        if not texto:
            return jsonify({"erro": "Texto não pode ser vazio!"}), 400
        if not tipo_modulacao:
            return jsonify({"erro": "O tipo de modulação não pode ser vazio!"}), 400
        if not enquadramento:
            return jsonify({"erro": "O método de enquadramento não pode ser vazio!"}), 400
        if porcentagem_erro < 0 or porcentagem_erro > 100:
            return jsonify({"erro": "Porcentagem de erro inválida! Use um valor entre 0 e 100."}), 400
        if not deteccao_erro:
            return jsonify({"erro": "O método de detecção de erro não pode ser vazio!"}), 400

        # 🔹 Debug: Exibe os dados recebidos
        print("📡 Recebendo dados para envio:")
        print(f"Texto: {texto}")
        print(f"Modulação: {tipo_modulacao}")
        print(f"Erro: {porcentagem_erro}%")
        print(f"Enquadramento: {enquadramento}")
        print(f"Detecção de erro: {deteccao_erro}")
        print(f"📡 Enviando para o receptor {host}:{port}")

        # 🔹 Inicia o processo de transmissão usando `enviar_dados`
        try:
            enviar_dados(
                HOST=host, 
                PORTA=port,  
                texto=texto, 
                tipo_modulacao=tipo_modulacao, 
                porcentagem_erro=porcentagem_erro, 
                enquadramento=enquadramento, 
                deteccao_erro=deteccao_erro  
            )
        except TypeError as te:
            print(f"🛑 ERRO: Tipo de parâmetros incorretos para `enviar_dados`: {te}")
            return jsonify({"erro": f"Erro de parâmetros: {te}"}), 400

        return jsonify({"mensagem": "Dados processados e enviados ao receptor com sucesso!"})

    except Exception as e:
        print(f"🛑 ERRO NO SERVIDOR: {str(e)}")
        return jsonify({"erro no servidor": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
