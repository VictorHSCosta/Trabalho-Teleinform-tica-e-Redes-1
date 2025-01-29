import socket

def iniciar_servidor():
    """
    Inicia o servidor para receber sinais do transmissor.
    """
    host = '0.0.0.0'
    port = 12345

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.bind((host, port))
            servidor.listen(1)
            print(f"Servidor socket escutando em {host}:{port}...")

            while True:
                conn, addr = servidor.accept()
                with conn:
                    print(f"Conexão estabelecida com {addr}")
                    dados = conn.recv(1024).decode('utf-8')
                    print(f"Dados recebidos: {dados}")
                    if ':' in dados:
                        tipo, sinal = dados.split(':', 1)
                        processar_sinal(sinal, tipo)
                    else:
                        print("Formato de mensagem inválido.")
    except Exception as e:
        print(f"Erro no servidor socket: {e}")

def processar_sinal(sinal, tipo):
    """
    Processa e exibe o sinal recebido.
    """
    print(f"Processando sinal do tipo {tipo}: {sinal}")
    # Adicione lógica de demodulação ou processamento adicional aqui
