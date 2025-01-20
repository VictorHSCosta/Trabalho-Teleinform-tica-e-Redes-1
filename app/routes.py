from flask import jsonify, render_template, request
from app import app
from app.backend.untils.bytecode import get_bytecode
from app.backend.functions.Enviar import *

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

@app.route('/enviar', methods=['GET'])
def enviar():
    erro = request.args.get('erro')  # Obtém o texto da query string
    text = request.args.get('bits') # Obtém o texto da query string
    tipo = request.args.get('tipo') # Obtém o texto da query string

    if not erro:
        return jsonify({"erro": "Erro não encontrado."}),400

    if not text:
        return jsonify({"erro": "Erro não encontrado."}),400
    
    try:
        enviarSinal(text)  
        return jsonify({"erro": text}),200
    except:
        return jsonify({"erro": "Erro na solicitação."}),400
        

if __name__ == '__main__':
    app.run(debug=True)