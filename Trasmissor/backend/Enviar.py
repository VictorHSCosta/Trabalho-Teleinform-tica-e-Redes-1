import socket
import json
from adicionar_erro import adicionar_erro
from conversores import texto_para_bits
from hamming import hamming_encode
from modulador import modular_nrz, modular_manchester, modular_bipolar

def enviar_dados(texto):
    # Configuração do cliente socket
    HOST = input("Digite o IP do servidor: ")  # O usuário pode digitar o IP do servidor Flask
    PORTA = 12345  # Mesma porta do servidor

    # Criar o socket
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORTA))

    # Entrada de texto
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

    # Criar JSON com os dados
    dados = {
        "sinal_modulado": sinal_modulado,
        "tipo_modulacao": tipo_modulacao
    }

    # Enviar para o servidor Flask via socket
    cliente.sendall(json.dumps(dados).encode())

    # Receber a resposta
    resposta = cliente.recv(4096).decode()
    resposta_json = json.loads(resposta)

    if "texto_recebido" in resposta_json:
        print("Texto decodificado recebido:", resposta_json["texto_recebido"])
    else:
        print("Erro:", resposta_json["erro"])

    cliente.close()

if __name__ == "__main__":
    enviar_dados()
