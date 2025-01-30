from flask import Flask, render_template, request, jsonify
import socket

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
    


if __name__ == "__main__":
    app.run(debug=True)
