def nrz_demodulacao(sinal):
    """Demodula um sinal NRZ para bits."""
    return [1 if bit == 1 else 0 for bit in sinal]

def bipolar_demodulacao(sinal):
    """Demodula um sinal Bipolar para bits."""
    return [1 if bit != 0 else 0 for bit in sinal]  # Bits não nulos são 1, zeros continuam zeros

def manchester_demodulacao(sinal):
    """Demodula um sinal Manchester para bits."""
    bits = []
    for i in range(0, len(sinal), 2):
        if sinal[i] == 1 and sinal[i + 1] == -1:
            bits.append(1)  # Padrão ↑↓ representa 1
        elif sinal[i] == -1 and sinal[i + 1] == 1:
            bits.append(0)  # Padrão ↓↑ representa 0
    return bits

def demodular_sinal(sinais_modulados, metodo):
    """Demodula os sinais recebidos de acordo com o método escolhido."""
    quadros_bits = []
    for sinal in sinais_modulados:
        if metodo == "NRZ":
            quadros_bits.append(nrz_demodulacao(sinal))
        elif metodo == "Bipolar":
            quadros_bits.append(bipolar_demodulacao(sinal))
        elif metodo == "Manchester":
            quadros_bits.append(manchester_demodulacao(sinal))
        else:
            raise ValueError("Método de demodulação inválido. Escolha 'NRZ', 'Bipolar' ou 'Manchester'.")
    return quadros_bits