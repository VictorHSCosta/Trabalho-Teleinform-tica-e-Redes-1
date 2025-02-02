# #primeira etapa do código de hamming, aquela q é feita no transmissor.

# def calcular_paridade(bits, indices):
#     """Calcula a paridade dos bits nos índices fornecidos."""
#     return sum(bits[i] for i in indices) % 2

# def codificar_hamming_31_26(bits):
#     """Codifica um bloco de 26 bits usando Hamming(31,26)."""
#     if len(bits) != 26:
#         raise ValueError("O bloco de entrada deve ter exatamente 26 bits.")

#     # Bits de paridade para Hamming(31,26)
#     p1 = calcular_paridade(bits, [0, 1, 3, 4, 6, 8, 10, 11, 13, 15, 17, 19, 21, 23, 25])
#     p2 = calcular_paridade(bits, [0, 2, 3, 5, 6, 9, 10, 12, 13, 16, 17, 20, 21, 24, 25])
#     p3 = calcular_paridade(bits, [1, 2, 3, 7, 8, 9, 10, 14, 15, 16, 17, 22, 23, 24, 25])
#     p4 = calcular_paridade(bits, [4, 5, 6, 7, 8, 9, 10, 18, 19, 20, 21, 22, 23, 24, 25])
#     p5 = calcular_paridade(bits, [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])

#     return [p1, p2, p3, p4, p5] + bits

# def aplicar_hamming_quadros(quadros):
#     """Aplica Hamming(31,26) a todos os quadros."""
#     return [codificar_hamming_31_26(quadro) for quadro in quadros]

# #Segunda parte do codigo de hamming, aquela q será feita no receptor

# def detectar_corrigir_hamming_31_26(bits):
#     """Decodifica um bloco de 31 bits corrigindo possíveis erros usando Hamming(31,26)."""
#     # Indices de bits de paridade
#     indices_paridade = [
#         [0, 1, 3, 4, 6, 8, 10, 11, 13, 15, 17, 19, 21, 23, 25],
#         [0, 2, 3, 5, 6, 9, 10, 12, 13, 16, 17, 20, 21, 24, 25],
#         [1, 2, 3, 7, 8, 9, 10, 14, 15, 16, 17, 22, 23, 24, 25],
#         [4, 5, 6, 7, 8, 9, 10, 18, 19, 20, 21, 22, 23, 24, 25],
#         [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
#     ]

#     # Calcula os bits de paridade recebidos
#     paridade_recebida = [bits[i] for i in range(5)]
    
#     # Calcula os bits de paridade esperados
#     paridade_calculada = [sum(bits[idx] for idx in indices) % 2 for indices in indices_paridade]

#     # Calcula o erro (posição errada)
#     erro_posicao = sum((2 ** i) * (paridade_recebida[i] ^ paridade_calculada[i]) for i in range(5)) - 1

#     # Se erro_posicao for maior ou igual a 0, há um erro que pode ser corrigido
#     if erro_posicao >= 0 and erro_posicao < 31:
#         bits[erro_posicao] ^= 1  # Corrige o erro invertendo o bit errado

#     # Retorna os 26 bits de dados corrigidos (ignorando os 5 bits de paridade)
#     return bits[5:]

# def corrigir_erros_quadros(quadros):
#     """Aplica a correção de erros de Hamming(31,26) em todos os quadros."""
#     quadros_corrigidos = [detectar_corrigir_hamming_31_26(quadro) for quadro in quadros]
#     return quadros_corrigidos


def codificar_hamming_31_26(dados):
    """
    Codifica um bloco de 26 bits usando o código de Hamming(31,26) com os bits de paridade
    nas posições 0, 1, 3, 7 e 15 (0-indexado), que correspondem às potências de 2 em sistema 1-indexado.
    
    Parâmetros:
        dados (list de int): lista com 26 bits (0 ou 1).
    
    Retorna:
        codeword (list de int): lista com 31 bits (código codificado).
    """
    if len(dados) != 26:
        raise ValueError("O bloco de entrada deve ter exatamente 26 bits.")
    
    # Posições reservadas para bits de paridade (0-indexado): 0 (1), 1 (2), 3 (4), 7 (8) e 15 (16)
    pos_paridade = {0, 1, 3, 7, 15}
    
    # Inicializa o codeword com 31 posições
    codeword = [None] * 31
    
    # Insere os dados nas posições que não são de paridade
    data_index = 0
    for i in range(31):
        if i in pos_paridade:
            codeword[i] = 0  # placeholder para o bit de paridade (será calculado)
        else:
            codeword[i] = dados[data_index]
            data_index += 1
    
    # Calcula cada bit de paridade
    # Para cada posição p de paridade, o valor a ser calculado é o XOR de todos os bits cujas posições (em 1-indexado)
    # possuam o bit correspondente a p+1 ativado.
    for p in pos_paridade:
        parity = 0
        mask = p + 1  # O bit de peso (p+1) em 1-indexado
        for j in range(31):
            # Se a posição j+1 tem o bit 'mask' ligado, inclui o bit na soma de paridade
            if (j + 1) & mask:
                # Exceto o próprio bit de paridade (na posição p)
                if j != p:
                    parity ^= codeword[j]
        codeword[p] = parity
    
    return codeword

def aplicar_hamming_quadros(quadros):
    """
    Aplica a codificação Hamming(31,26) a uma lista de quadros de 26 bits.
    
    Parâmetros:
        quadros (list de list de int): cada quadro é uma lista com 26 bits.
    
    Retorna:
        Lista de quadros codificados (cada um com 31 bits).
    """
    return [codificar_hamming_31_26(quadro) for quadro in quadros]

def detectar_corrigir_hamming_31_26(codeword):
    """
    Recebe um quadro de 31 bits (que pode ter sofrido um erro único) e realiza:
      1. Cálculo do síndrome usando as posições de paridade.
      2. Correção do erro, se detectado.
      3. Extração dos 26 bits de dados originais.
    
    Parâmetros:
        codeword (list de int): lista com 31 bits.
    
    Retorna:
        dados (list de int): lista com os 26 bits corrigidos de dados.
    """
    if len(codeword) != 31:
        raise ValueError("O quadro de entrada deve ter exatamente 31 bits.")
    
    pos_paridade = [0, 1, 3, 7, 15]
    syndrome = 0
    
    # Calcula o síndrome: para cada posição de paridade, recalcula o XOR de todos os bits que participam dela.
    # Se o resultado for 1, soma o peso (p+1) ao síndrome.
    for p in pos_paridade:
        parity = 0
        mask = p + 1
        for j in range(31):
            if (j + 1) & mask:
                parity ^= codeword[j]
        if parity != 0:
            syndrome += (p + 1)
    
    # Se o síndrome não for zero, há um erro na posição indicada pelo valor (em 1-indexado).
    if syndrome != 0:
        erro_index = syndrome - 1  # converte para 0-indexado
        if erro_index < 31:
            codeword[erro_index] ^= 1  # Corrige o erro invertendo o bit
    
    # Extrai os bits de dados (todas as posições que não são de paridade)
    dados = []
    for i in range(31):
        if i not in pos_paridade:
            dados.append(codeword[i])
    return dados

def corrigir_erros_quadros(quadros):
    """
    Aplica a decodificação e correção de erros Hamming(31,26) em uma lista de quadros.
    
    Parâmetros:
        quadros (list de list de int): cada quadro é uma lista com 31 bits.
    
    Retorna:
        Lista de quadros corrigidos, onde cada quadro possui 26 bits de dados.
    """
    # Utilizamos uma cópia do quadro (quadro[:]) para evitar modificar o original
    return [detectar_corrigir_hamming_31_26(quadro[:]) for quadro in quadros]


# Exemplo de uso:

if __name__ == '__main__':
        # Mensagem original codificada
    dados_exemplo = [1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 
                    1, 1, 0, 1, 0, 0, 1, 1, 0, 1,
                    0, 1, 1, 0, 0, 1]  # Deve ter 26 bits

    # Codificando com Hamming
    codeword = codificar_hamming_31_26(dados_exemplo)

    # Inserindo um erro (invertendo um bit)
    erro_posicao = 10  # Teste com outras posições
    codeword_com_erro = codeword[:]
    codeword_com_erro[erro_posicao] ^= 1

    print("Codeword com erro:", codeword_com_erro)

    # Tentando corrigir
    dados_corrigidos = detectar_corrigir_hamming_31_26(codeword_com_erro)

    print("Dados corrigidos:", dados_corrigidos)
    print("Mensagem original era igual?", dados_corrigidos == dados_exemplo)

