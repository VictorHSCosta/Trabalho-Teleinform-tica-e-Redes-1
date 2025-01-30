def texto_para_bits(texto):
    """Converte uma string de texto em uma lista de bits."""
    return [int(bit) for char in texto for bit in f"{ord(char):08b}"]

def bits_para_texto(bits):
    """
    Converte uma lista de bits em uma string de texto.
    :param bits: Lista de bits (0 ou 1).
    :return: String de texto correspondente.
    """
    if len(bits) % 8 != 0:
        raise ValueError("O número de bits deve ser múltiplo de 8 para conversão.")
    chars = [chr(int("".join(map(str, bits[i:i + 8])), 2)) for i in range(0, len(bits), 8)]
    return "".join(chars)
