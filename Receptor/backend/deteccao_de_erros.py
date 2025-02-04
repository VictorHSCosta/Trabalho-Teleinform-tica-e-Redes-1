import binascii

### 🔹 DETECÇÃO DE ERROS - BIT DE PARIDADE ###

def calcular_paridade(bits):
    """Calcula o bit de paridade (paridade par)."""
    return sum(bits) % 2

def adicionar_paridade(bloco):
    """Adiciona um bit de paridade ao final do bloco."""
    bit_paridade = calcular_paridade(bloco)
    return bloco + [bit_paridade]

def verificar_paridade(bloco):
    """Verifica se o bit de paridade está correto."""
    bit_paridade = bloco[-1]  # Último bit é o bit de paridade
    bloco_sem_paridade = bloco[:-1]  # Remove o bit de paridade para verificar
    return calcular_paridade(bloco_sem_paridade) == bit_paridade

### 🔹 DETECÇÃO DE ERROS - CRC-32 ###

def calcular_crc32(bits):
    """Calcula o CRC-32 de um conjunto de bits."""
    byte_array = bytearray(int("".join(map(str, bits)), 2).to_bytes((len(bits) + 7) // 8, byteorder='big'))
    crc = binascii.crc32(byte_array) & 0xFFFFFFFF  # Aplica máscara para garantir 32 bits
    return list(map(int, format(crc, '032b')))  # Retorna CRC-32 como lista de bits

def adicionar_crc32(bloco):
    """Adiciona o CRC-32 ao final do bloco."""
    crc_bits = calcular_crc32(bloco)
    return bloco + crc_bits

def verificar_crc32(bloco):
    """Verifica se o CRC-32 está correto."""
    dados = bloco[:-32]  # Remove os 32 bits do CRC
    crc_recebido = bloco[-32:]  # Últimos 32 bits são o CRC
    crc_calculado = calcular_crc32(dados)
    return crc_recebido == crc_calculado

### 🔹 APLICAÇÃO DA DETECÇÃO DE ERROS APÓS O DESENQUADRAMENTO ### ESSA É A PARTE DO RECEPTOR.

def detectar_erros_quadros(quadros, metodo):
    """Aplica a detecção de erros usando Bit de Paridade ou CRC-32."""
    
    # Mapeia o nome do método à função correspondente.
    metodos = {
        "Paridade": verificar_paridade,
        "CRC-32": verificar_crc32
    }
    
    if metodo not in metodos:
        raise ValueError("Método de detecção inválido. Escolha 'Paridade' ou 'CRC-32'.")
    
    funcao_verificacao = metodos[metodo]
    
    for i, quadro in enumerate(quadros):
        if funcao_verificacao(quadro):
            print(f"✅ Quadro {i+1}: Sem erros ({metodo} OK)")
        else:
            print(f"❌ Quadro {i+1}: Erro detectado ({metodo} inválido!)")

def remover_crc32(bits):
    """
    Remove os 32 bits finais (CRC-32) de um conjunto de bits e retorna apenas os bits originais.
    """
    if len(bits) <= 32:
        raise ValueError("O conjunto de bits é muito pequeno para conter um CRC-32.")

    # Passo 1: Separar a parte da mensagem e a parte do CRC
    bits_sem_crc = bits[:-32]  # Remove os últimos 32 bits

    return bits_sem_crc  # Retorna apenas os bits originais sem o CRC






