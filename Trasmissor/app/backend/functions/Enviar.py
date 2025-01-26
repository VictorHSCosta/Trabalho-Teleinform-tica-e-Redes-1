import socket
from random import randint

def calcularErro(text, erro=0):
    """
    Aplica um erro aleatório ao trem de bits.
    """
    # Remove espaços e sanitiza a entrada
    text = text.strip().replace(" ", "")
    text = [int(bit) for bit in text if bit.isdigit()]  # Garante que apenas números são usados

    if not text:
        raise ValueError("O trem de bits está vazio ou inválido.")

    # Converte erro para inteiro, caso esteja como string
    erro = int(erro)

    # Aplica erro aleatório
    if randint(0, 100) < erro:
        posicao = randint(0, len(text) - 1)
        text[posicao] = 1 if text[posicao] == 0 else 0
        print(f"Erro inserido na posição: {posicao}")
    return text



def enviarSinal(bits, erro, tipo):
    """
    Aplica erro ao trem de bits, modula o sinal e envia ao receptor.
    """
    bits_com_erro = calcularErro(bits, erro)
    sinal = ''.join(map(str, bits_com_erro))  # Converte bits para string

    # Envia o sinal via socket
    enviar_para_receptor(sinal, tipo)

def enviar_para_receptor(sinal, tipo):
    """
    Envia o sinal ao receptor via socket.
    """
    host = '192.168.100.8'  # Substitua pelo IP do receptor
    port = 12345  # Porta do receptor

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((host, port))
            mensagem = f"{tipo}:{sinal}"  # Inclui o tipo de modulação
            cliente.sendall(mensagem.encode('utf-8'))
            print(f"Sinal enviado ao receptor: {mensagem}")
    except Exception as e:
        print(f"Erro ao conectar ao receptor: {e}")
        raise
