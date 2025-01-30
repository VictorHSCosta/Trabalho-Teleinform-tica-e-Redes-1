def hamming_encode(data):
    data_bits = list(map(int, data))
    n = len(data_bits)
    encoded = []
    
    # Calculando o número de bits de paridade
    m = 0
    while (2 ** m) < (n + m + 1):
        m += 1

    # Inserindo os bits de dados e placeholders para paridade
    j = 0
    for i in range(1, n + m + 1):
        if i & (i - 1) == 0:  # Potência de 2
            encoded.append(0)  # Placeholder para bits de paridade
        else:
            encoded.append(data_bits[j])
            j += 1

    # Calculando os valores dos bits de paridade
    for i in range(m):
        paridade = 0
        for j in range(1, len(encoded) + 1):
            if j & (1 << i) != 0:
                paridade ^= encoded[j - 1]
        encoded[(1 << i) - 1] = paridade  # Atualizando o bit de paridade

    return ''.join(map(str, encoded))


def hamming_decode(received):
    received_bits = list(map(int, received))
    n = len(received_bits)

    # Calcular o síndrome
    syndrome = 0
    error_bits = []  # Para armazenar as posições de erro

    for i in range(n):
        if (i + 1) & (i + 1) - 1 == 0:  # Potência de 2
            paridade = 0
            for j in range(n):
                if (j + 1) & (i + 1) != 0:
                    paridade ^= received_bits[j]
            if paridade != 0:
                syndrome += i + 1
                error_bits.append(i + 1)

    # Verificar se mais de um erro foi detectado
    if len(error_bits) > 1:
        print(f"Erros múltiplos detectados nas posições: {error_bits}")
        print("O código de Hamming não pode corrigir múltiplos erros.")
        return ''.join(map(str, received_bits))  # Retorna os bits sem corrigir

    # Corrigir o erro, se necessário
    if syndrome > 0 and syndrome <= n:
        print(f"Erro detectado na posição: {syndrome}")
        received_bits[syndrome - 1] ^= 1  # Inverter o bit
    else:
        print("Nenhum erro detectado ou posição inválida.")

    # Remover os bits de paridade para reconstruir os dados originais
    decoded = []
    for i in range(1, n + 1):
        if i & (i - 1) != 0:  # Não é potência de 2
            decoded.append(received_bits[i - 1])

    return ''.join(map(str, decoded))





