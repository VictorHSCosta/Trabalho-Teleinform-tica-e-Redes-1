import numpy as np

def nrz_modulacao(bits):
    """Modula os bits usando NRZ (Non-Return-to-Zero)."""
    return np.array([1 if bit == 1 else -1 for bit in bits])

def bipolar_modulacao(bits):
    """Modula os bits usando codificação Bipolar."""
    bipolar = []
    last = -1  # Começa com -1, pois alterna entre -1 e +1
    for bit in bits:
        if bit == 1:
            last = -last
            bipolar.append(last)
        else:
            bipolar.append(0)
    return np.array(bipolar)

def manchester_modulacao(bits):
    """Modula os bits usando Manchester."""
    manchester = []
    for bit in bits:
        if bit == 1:
            manchester.extend([1, -1])  # Sobe depois desce
        else:
            manchester.extend([-1, 1])  # Desce depois sobe
    return np.array(manchester)

def modular_quadros(quadros, metodo):
    """Aplica a modulação escolhida (NRZ, Bipolar ou Manchester) a todos os quadros."""
    sinais = []
    for quadro in quadros:
        if metodo == "NRZ":
            sinais.append(nrz_modulacao(quadro))
        elif metodo == "Bipolar":
            sinais.append(bipolar_modulacao(quadro))
        elif metodo == "Manchester":
            sinais.append(manchester_modulacao(quadro))
        else:
            raise ValueError("Método de modulação inválido. Escolha entre 'NRZ', 'Bipolar' ou 'Manchester'.")
    return sinais