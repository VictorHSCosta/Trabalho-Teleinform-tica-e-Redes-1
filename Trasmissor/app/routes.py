from flask import jsonify, render_template, request
from app import app
from app.backend.untils.bytecode import get_bytecode
from app.backend.functions.Enviar import enviarSinal

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_bits', methods=['GET'])
def get_bits():
    text = request.args.get('text')  # Obtém o texto digitado
    if not text:
        return jsonify({"bits_array": "Texto não encontrado."}), 400
    
    # Transforma o texto em um trem de bits
    bits_array = get_bytecode(text)
    return jsonify({"bits_array": bits_array})

@app.route('/enviar', methods=['POST'])
def enviar():
    try:
        data = request.get_json()
        erro = data.get('erro')
        bits = data.get('bits')
        tipo = data.get('tipo')

        # Verifique se os parâmetros estão presentes
        if erro is None or bits is None or tipo is None:
            return jsonify({"erro": "Parâmetros faltando: 'erro', 'bits' ou 'tipo'."}), 400

        # Converte 'erro' para inteiro, se necessário
        erro = int(erro)

        # Valida os bits
        if not all(bit in '01' for bit in bits.replace(" ", "")):
            return jsonify({"erro": "O trem de bits contém caracteres inválidos."}), 400

        # Chamar a função para enviar o sinal
        enviarSinal(bits, erro, tipo)
        return jsonify({"mensagem": "Sinal enviado com sucesso!"}), 200
    except ValueError as ve:
        print(f"Erro de valor: {ve}")
        return jsonify({"erro": f"Erro de valor: {ve}"}), 400
    except Exception as e:
        print(f"Erro ao enviar sinal: {e}")
        return jsonify({"erro": f"Erro ao processar envio: {e}"}), 400



if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Porta do transmissor
