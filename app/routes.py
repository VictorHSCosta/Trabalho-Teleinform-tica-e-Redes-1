from flask import jsonify, render_template, request
from app import app
from app.backend.untils.bytecode import get_bytecode

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_bits', methods=['GET'])
def get_bits():
    text = request.args.get('text')  # Obtém o texto da query string
    if not text:
        return jsonify({"error": "Texto não fornecido"}), 400
    
    bits_array = get_bytecode(text)
    return jsonify({"bits_array": bits_array})

if __name__ == '__main__':
    app.run(debug=True)