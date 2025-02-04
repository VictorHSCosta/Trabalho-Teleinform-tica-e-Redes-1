def calcular_paridade(bits, indices):
    """Calcula a paridade dos bits nos índices fornecidos."""
    return sum(bits[i] for i in indices) % 2

def codificar_hamming_31_26(bits):
    """Codifica um bloco de 26 bits usando Hamming(31,26)."""
    if len(bits) != 26:
        raise ValueError("O bloco de entrada deve ter exatamente 26 bits.")

    p1 = calcular_paridade(bits, [0, 1, 3, 4, 6, 8, 10, 11, 13, 15, 17, 19, 21, 23, 25])
    p2 = calcular_paridade(bits, [0, 2, 3, 5, 6, 9, 10, 12, 13, 16, 17, 20, 21, 24, 25])
    p3 = calcular_paridade(bits, [1, 2, 3, 7, 8, 9, 10, 14, 15, 16, 17, 22, 23, 24, 25])
    p4 = calcular_paridade(bits, [4, 5, 6, 7, 8, 9, 10, 18, 19, 20, 21, 22, 23, 24, 25])
    p5 = calcular_paridade(bits, [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])

    return [p1, p2, p3, p4, p5] + bits

def aplicar_hamming_quadros(quadros):
    """Aplica Hamming(31,26) a todos os quadros."""
    return [codificar_hamming_31_26(quadro) for quadro in quadros]

#Segunda parte de hamming, Receptor.

def detectar_corrigir_hamming_31_26(bits):
    """Decodifica um bloco de 31 bits corrigindo possíveis erros usando Hamming(31,26)."""
    indices_paridade = [
        [0, 1, 3, 4, 6, 8, 10, 11, 13, 15, 17, 19, 21, 23, 25],
        [0, 2, 3, 5, 6, 9, 10, 12, 13, 16, 17, 20, 21, 24, 25],
        [1, 2, 3, 7, 8, 9, 10, 14, 15, 16, 17, 22, 23, 24, 25],
        [4, 5, 6, 7, 8, 9, 10, 18, 19, 20, 21, 22, 23, 24, 25],
        [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    ]

    paridade_recebida = [bits[i] for i in range(5)]
    paridade_calculada = [sum(bits[idx] for idx in indices) % 2 for indices in indices_paridade]
    erro_posicao = sum((2 ** i) * (paridade_recebida[i] ^ paridade_calculada[i]) for i in range(5)) - 1

    if 0 <= erro_posicao < 31:
        bits[erro_posicao] ^= 1

    return bits[5:]

def corrigir_erros_quadros(quadros):
    """Aplica a correção de erros de Hamming(31,26) em todos os quadros."""
    return [detectar_corrigir_hamming_31_26(quadro) for quadro in quadros]
