def demodular_nrz(sinal, amostras_por_bit=100):
    """
    Demodula um sinal NRZ que usa -1 e 1 para representar 0 e 1.
    :param sinal: Lista de valores representando o sinal modulado.
    :param amostras_por_bit: Número de amostras por bit no sinal digital.
    :return: Lista de bits (0 ou 1).
    """
    bits = []
    for i in range(0, len(sinal), amostras_por_bit):
        media = sum(sinal[i:i + amostras_por_bit]) / amostras_por_bit
        bits.append(0 if media < 0 else 1)
    return bits

def demodular_manchester(sinal, amostras_por_bit=100):
    """
    Demodula um sinal Manchester em bits.
    :param sinal: Lista representando o sinal modulado.
    :param amostras_por_bit: Número de amostras por bit no sinal digital.
    :return: Lista de bits demodulados.
    """
    if len(sinal) % amostras_por_bit != 0:
        raise ValueError("O sinal Manchester deve ter um comprimento múltiplo de amostras_por_bit.")

    bits = []
    metade = amostras_por_bit // 2
    for i in range(0, len(sinal), amostras_por_bit):
        primeiro_meio = sum(sinal[i:i + metade]) / metade
        segundo_meio = sum(sinal[i + metade:i + amostras_por_bit]) / metade
        if primeiro_meio < segundo_meio:  # Transição 0 -> 1
            bits.append(0)
        elif primeiro_meio > segundo_meio:  # Transição 1 -> 0
            bits.append(1)
        else:
            raise ValueError("Erro no sinal Manchester: transição inválida detectada.")
    return bits

def demodular_bipolar(sinal, amostras_por_bit=100):
    """
    Demodula um sinal bipolar em bits.
    :param sinal: Lista de valores representando o sinal modulado.
    :param amostras_por_bit: Número de amostras por bit no sinal digital.
    :return: Lista de bits (0 ou 1).
    """
    bits = []
    for i in range(0, len(sinal), amostras_por_bit):
        media = sum(sinal[i:i + amostras_por_bit]) / amostras_por_bit
        bits.append(1 if abs(media) > 0 else 0)
    return bits

