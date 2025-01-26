import socket
from random import randint
from app.backend.untils.digital import GeradorSinalDigital


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
    # Adiciona erro ao trem de bits
    bits_com_erro = calcularErro(bits, erro)

    # Cria uma instância da classe GeradorSinalDigital
    gerador = GeradorSinalDigital()
    gerador.definir_fluxo_bits(bits_com_erro)
    gerador.definir_tensao(1)  # Define a amplitude do sinal (mínimo = -1, máximo = 1)

    # Gera o sinal com base no tipo de modulação
    if tipo == "NRZ":
        tempo, sinal = gerador.gerar_nrz()
    elif tipo == "Manchester":
        tempo, sinal = gerador.gerar_manchester()
    elif tipo == "Bipolar":
        tempo, sinal = gerador.gerar_bipolar()
    else:
        raise ValueError("Tipo de modulação inválido. Escolha entre 'NRZ', 'Manchester' ou 'Bipolar'.")

    # Envia o sinal modulado ao receptor
    enviar_para_receptor(sinal, tipo)

def enviar_para_receptor(sinal, tipo):
    """
    Envia o sinal modulado ao receptor via socket.
    """
    host = '192.168.100.8'  # Substitua pelo IP do receptor
    port = 12345  # Porta do receptor

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((host, port))
            # Converte o sinal modulado em string para envio
            mensagem = f"{tipo}:{','.join(map(str, sinal))}"  # Separa os valores do sinal por vírgulas
            cliente.sendall(mensagem.encode('utf-8'))
            print(f"Sinal enviado ao receptor: {mensagem}")
    except Exception as e:
        print(f"Erro ao conectar ao receptor: {e}")
        raise
