from flask import jsonify, render_template
from app import app
from app.backend.functions.Receber import iniciar_servidor
from app.backend.functions.Receber import processar_e_corrigir_sinal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/receber', methods=['GET'])
def receber():
    tipo, sinal = iniciar_servidor()
    if tipo is None or sinal is None:
        return jsonify({"erro": "Erro ao processar os dados recebidos."}), 400

    # Continue com o processamento normal
    bits_destacados, bits_corrigidos = processar_e_corrigir_sinal(sinal, tipo)
    return jsonify({
        "bits_com_erro": bits_destacados,
        "bits_corrigidos": ''.join(map(str, bits_corrigidos)),
    })
@app.route('/resultado', methods=['GET'])
def resultado():
    try:
        resultado = iniciar_servidor()
        if resultado:
            return jsonify(resultado), 200
        else:
            return jsonify({"erro": "Erro no processamento do sinal."}), 400
    except Exception as e:
        return jsonify({"erro": f"Erro inesperado: {str(e)}"}), 500