import random

def adicionar_erro(bits, porcentagem_erro):
    """
    Adiciona erros ao trem de bits com base em uma porcentagem definida.
    :param bits: Lista de bits (0 e 1).
    :param porcentagem_erro: Porcentagem de erros a serem introduzidos (0-100).
    :return: Lista de bits com erros adicionados.
    """
    total_erros = int(len(bits) * porcentagem_erro / 100)
    indices = random.sample(range(len(bits)), total_erros)
    for i in indices:
        bits[i] = 1 if bits[i] == 0 else 0  # Inverte o bit
    return bits
