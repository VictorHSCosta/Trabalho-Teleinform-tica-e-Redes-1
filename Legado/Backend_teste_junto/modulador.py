import numpy as np

def modular_nrz(bits, amostras_por_bit=100):
    """
    Modula um trem de bits em NRZ e gera um sinal digital contínuo.
    :param bits: Lista de bits (0 ou 1).
    :param amostras_por_bit: Número de amostras por bit no sinal digital.
    :return: Lista representando o sinal digital contínuo.
    """
    sinal = []
    for bit in bits:
        valor = -1 if bit == 0 else 1
        sinal.extend([valor] * amostras_por_bit)  # Repete o valor para cada amostra
    return sinal

def modular_manchester(bits, amostras_por_bit=100):
    """
    Modula um trem de bits em Manchester e gera um sinal digital contínuo.
    :param bits: Lista de bits (0 ou 1).
    :param amostras_por_bit: Número de amostras por bit no sinal digital.
    :return: Lista representando o sinal digital contínuo.
    """
    sinal = []
    metade = amostras_por_bit // 2
    for bit in bits:
        if bit == 0:
            sinal.extend([0] * metade + [1] * metade)  # Transição 0 -> 1
        else:
            sinal.extend([1] * metade + [0] * metade)  # Transição 1 -> 0
    return sinal

def modular_bipolar(bits, amostras_por_bit=100):
    """
    Modula um trem de bits em bipolar e gera um sinal digital contínuo.
    :param bits: Lista de bits (0 ou 1).
    :param amostras_por_bit: Número de amostras por bit no sinal digital.
    :return: Lista representando o sinal digital contínuo.
    """
    sinal = []
    toggle = 1
    for bit in bits:
        if bit == 1:
            sinal.extend([toggle] * amostras_por_bit)
            toggle *= -1
        else:
            sinal.extend([0] * amostras_por_bit)
    return sinal

