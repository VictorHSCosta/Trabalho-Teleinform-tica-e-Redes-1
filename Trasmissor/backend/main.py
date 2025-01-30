from backend.adicionar_erro import adicionar_erro
from backend.conversores import texto_para_bits, bits_para_texto
from backend.hamming import hamming_encode, hamming_decode
from backend.demodulador import demodular_nrz, demodular_manchester, demodular_bipolar
from modulador import modular_nrz, modular_manchester, modular_bipolar

def main():
    # Entrada de texto
    texto = input("Digite o texto a ser transmitido: ")
    bits = texto_para_bits(texto)
    print(f"Texto convertido para bits: {bits}")

    # Codificação Hamming
    bits_codificados = hamming_encode(bits)
    print(f"Bits codificados com Hamming: {bits_codificados}")

    # Adicionar erros
    porcentagem_erro = float(input("Digite a porcentagem de erro a ser adicionada (0-100): "))
    bits_com_erro = adicionar_erro(list(map(int, bits_codificados)), porcentagem_erro)
    print(f"Bits com erro: {bits_com_erro}")

    # Escolha da modulação
    tipo_modulacao = input("Escolha a modulação (NRZ, Manchester, Bipolar): ").lower()
    amostras_por_bit = int(input("Digite o número de amostras por bit: "))

    if tipo_modulacao == "nrz":
        sinal_modulado = modular_nrz(bits_com_erro, amostras_por_bit)
    elif tipo_modulacao == "manchester":
        sinal_modulado = modular_manchester(bits_com_erro, amostras_por_bit)
    elif tipo_modulacao == "bipolar":
        sinal_modulado = modular_bipolar(bits_com_erro, amostras_por_bit)
    else:
        print("Modulação inválida!")
        return

    print(f"Sinal modulado: {sinal_modulado}")

    # Demodulação
    if tipo_modulacao == "nrz":
        bits_demodulados = demodular_nrz(sinal_modulado, amostras_por_bit)
    elif tipo_modulacao == "manchester":
        bits_demodulados = demodular_manchester(sinal_modulado, amostras_por_bit)
    elif tipo_modulacao == "bipolar":
        bits_demodulados = demodular_bipolar(sinal_modulado, amostras_por_bit)
    else:
        print("Demodulação inválida!")
        return

    print(f"Bits demodulados: {bits_demodulados}")

    # Correção de erros
    bits_corrigidos = hamming_decode(''.join(map(str, bits_demodulados)))
    print(f"Bits corrigidos: {bits_corrigidos}")

    # Verificar se os bits corrigidos são múltiplos de 8
    if len(bits_corrigidos) % 8 != 0:
        print("Erro: O número de bits corrigidos não é múltiplo de 8.")
        return

    # Conversão para texto
    try:
        texto_recebido = bits_para_texto(list(map(int, bits_corrigidos)))
        print(f"Texto recebido: {texto_recebido}")
    except ValueError as e:
        print(f"Erro na conversão de bits para texto: {e}")

if __name__ == "__main__":
    main()
