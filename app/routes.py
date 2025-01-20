from flask import jsonify, render_template, request
from app import app
from app.backend.untils.bytecode import get_bytecode
from app.backend.functions.Enviar import enviarSinal

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

@app.route('/enviar', methods=['POST'])
def enviar():
    data = request.get_json()  # Pega os dados JSON enviados pelo frontend

    erro = data.get('erro')  
    text = data.get('bits')
    tipo = data.get('tipo')

    if erro is None:
        return jsonify({"erro": "O parâmetro 'erro' não foi enviado."}), 400

    if text is None:
        return jsonify({"erro": "O parâmetro 'bits' não foi enviado."}), 400

    if tipo is None:
        return jsonify({"erro": "O parâmetro 'tipo' não foi enviado."}), 400

    try:
        enviarSinal(text, erro)  
        return jsonify({"mensagem": f"Sinal enviado com sucesso: {text}"}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro na solicitação: {str(e)}"}), 400


if __name__ == '__main__':
    app.run(debug=True)