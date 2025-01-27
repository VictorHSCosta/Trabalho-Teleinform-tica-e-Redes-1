from app import app
from threading import Thread
from app.backend.functions.Receber import iniciar_servidor
import os

def start_socket_server():
    """
    Inicia o servidor socket em uma thread separada.
    """
    print("Iniciando servidor socket...")
    iniciar_servidor()

if __name__ == '__main__':
    # Inicia o servidor socket somente no processo principal
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        socket_thread = Thread(target=start_socket_server, daemon=True)
        socket_thread.start()

    # Inicia o servidor Flask
    app.run(debug=True, port=5000)
