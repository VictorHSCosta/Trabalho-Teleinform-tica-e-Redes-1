def texto_para_bits(texto):
    """Converte uma string de texto em uma lista de bits usando UTF-8."""
    return [int(bit) for byte in texto.encode('utf-8') for bit in f"{byte:08b}"]


def bits_para_texto(bits):
    """
    Converte uma lista de bits em uma string de texto UTF-8.
    :param bits: Lista de bits (0 ou 1).
    :return: String de texto correspondente em UTF-8.
    """
    if len(bits) % 8 != 0:
        raise ValueError("O número de bits deve ser múltiplo de 8 para conversão.")
    
    # Converte a lista de bits para uma sequência de bytes
    bytes_data = bytes(int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8))
    
    try:
        return bytes_data.decode("utf-8", errors="replace")  # Decodifica corretamente para UTF-8, substituindo erros
    except UnicodeDecodeError:
        raise ValueError("Os bits fornecidos não formam uma sequência válida em UTF-8.")
    
def decimal_para_bits(decimal_array):
    """Converte um array de valores decimais UTF-8 em uma lista contínua de bits."""
    bits = []
    for valor in decimal_array:
        bits.extend([int(b) for b in format(valor, '08b')])  # Converte para binário e adiciona os bits à lista
    return bits

def bits_para_decimal(bits_array):
    """Converte um array contínuo de bits em um array de valores decimais UTF-8."""
    if len(bits_array) % 8 != 0:
        raise ValueError("O número de bits não é múltiplo de 8.")  # Garantia de bytes completos
    
    decimal_array = []
    for i in range(0, len(bits_array), 8):
        byte = bits_array[i:i+8]  # Pega um grupo de 8 bits
        decimal_array.append(int("".join(map(str, byte)), 2))  # Converte para decimal
    
    return decimal_array


def padronizar_bits(bits_array):
    # Calcula quantos bits faltam para completar um byte
    print("Opaaaaaaaaa")
    print(bits_array)

    resto = len(bits_array) % 8
    if resto != 0:
        padding = [0] * (8 - resto)
        bits_array.extend(padding)
    return bits_array





if __name__ == "__main__":
    # Teste de conversão de texto para bits
    texto = "Olá, Mundo! 😊"
    bits = texto_para_bits(texto)
    print(f"Texto: {texto}")
    print(f"Bits: {bits}")

    # Teste de conversão de bits para texto
    texto_recuperado = bits_para_texto(bits)
    print(f"Texto recuperado: {texto_recuperado}")
    print(f"Texto igual ao original: {texto == texto_recuperado}")

    utf8_bytes = [100, 107, 126, 252, 72, 101, 108, 177, 108, 111, 44, 32, 87, 111, 114, 10, 108, 100, 33, 32, 240, 159, 152, 138, 126, 0, 0]

    # Convertendo para bits
    array_de_bits = decimal_para_bits(utf8_bytes)

    # Exibindo resultado
    print(array_de_bits)


