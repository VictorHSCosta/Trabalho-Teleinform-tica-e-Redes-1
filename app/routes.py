from flask import jsonify, render_template, request
from app import app
from app.backend.untils.bytecode import get_bytecode
from app.backend.functions.erro import set_erro

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
    text = request.args.get('erro')  # Obtém o texto da query string
    if not text:
        text = 0
    
    try:
        set_erro(text)
        return jsonify({"erro": text}),200
    except:
        return jsonify({"erro": "Erro na solicitação."}),400



if __name__ == '__main__':
    app.run(debug=True)