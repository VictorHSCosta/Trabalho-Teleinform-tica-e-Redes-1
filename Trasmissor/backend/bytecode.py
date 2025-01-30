# Data: 2021-09-12
# Descrição: Arquivo responsável por converter texto em bytecode
#

from .config import run

def get_bits_array(text):
        """
        Retorna um array onde cada bit é uma casa do array.
        """
        binary_representation = ''.join(format(ord(char), '08b') for char in text)
        return [int(bit) for bit in binary_representation]

def get_seven_bit_chunks(text):
        
        binary_representation = ''.join(format(ord(char), '08b') for char in text)
        # Divide a representação binária em chunks de 7 bits
        chunks = [binary_representation[i:i+7] for i in range(0, len(binary_representation), 8)]
        return ' '.join(chunks)


def get_bytecode(text):

    bytecode = []
    textBytecode = ""

    bytecode = get_bits_array(text)
    textBytecode = get_seven_bit_chunks(text)
    run(bytecode)

    return textBytecode




    
    