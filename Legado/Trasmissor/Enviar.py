from Backend_teste_junto.adicionar_erro import adicionar_erro
from Backend_teste_junto.conversores import texto_para_bits
from Backend_teste_junto.hamming import hamming_encode
from Backend_teste_junto.modulador import modular_nrz, modular_manchester, modular_bipolar
import socket

def enviar_dados():
    # Configuração do socket
    host = '127.0.0.1'  # Endereço do servidor (localhost)
    porta = 12345       # Porta para comunicação
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, porta))

    # Entrada de texto
    texto = input("Digite o texto a ser transmitido: ")
    bits = texto_para_bits(texto)
    print(f"Texto convertido para bits: {bits}")

    # Codificação Hamming
    bits_codificados = hamming_encode(bits)
    print(f"Bits codificados com Hamming: {bits_codificados}")

    # Adicionar erros (opcional)
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

    # Enviar dados para o receptor
    cliente.sendall(str(sinal_modulado).encode())
    print("Sinal enviado ao receptor.")
    cliente.close()

if __name__ == "__main__":
    enviar_dados()
