from flask import jsonify, render_template
from app import app
from app.backend.functions.Enviar import iniciar_servidor

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/receber', methods=['GET'])
def receber():
    sinal = iniciar_servidor()
    return jsonify({"mensagem_recebida": sinal})

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Porta do receptor
