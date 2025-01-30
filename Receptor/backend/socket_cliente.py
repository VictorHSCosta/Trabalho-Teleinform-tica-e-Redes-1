import socket
import json
from adicionar_erro import adicionar_erro
from conversores import texto_para_bits
from hamming import hamming_encode
from modulador import modular_nrz, modular_manchester, modular_bipolar

def enviar_dados(ip_servidor):
    PORTA = 12345  # Porta fixa do servidor Flask

    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((ip_servidor, PORTA))

        texto = input("Digite o texto a ser transmitido: ")
        bits = texto_para_bits(texto)
        print(f"Texto convertido para bits: {bits}")

        bits_codificados = hamming_encode(bits)
        print(f"Bits codificados com Hamming: {bits_codificados}")

        porcentagem_erro = float(input("Digite a porcentagem de erro a ser adicionada (0-100): "))
        bits_com_erro = adicionar_erro(list(map(int, bits_codificados)), porcentagem_erro)
        print(f"Bits com erro: {bits_com_erro}")

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

        dados = {
            "sinal_modulado": sinal_modulado,
            "tipo_modulacao": tipo_modulacao
        }

        cliente.sendall(json.dumps(dados).encode())

        resposta = cliente.recv(4096).decode()
        resposta_json = json.loads(resposta)

        if "texto_recebido" in resposta_json:
            print("Texto decodificado recebido:", resposta_json["texto_recebido"])
        else:
            print("Erro:", resposta_json["erro"])

        cliente.close()
    
    except socket.error as e:
        print("Erro na conexão:", e)

if __name__ == "__main__":
    ip = input("Digite o IP do servidor: ")
    enviar_dados(ip)
