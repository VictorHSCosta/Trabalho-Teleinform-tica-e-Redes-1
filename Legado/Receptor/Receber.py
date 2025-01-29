from ..Backend_teste_junto.conversores import bits_para_texto
from ..Backend_teste_junto.hamming import hamming_decode
from ..Backend_teste_junto.demodulador import demodular_nrz, demodular_manchester, demodular_bipolar
import socket

def receber_dados():
    # Configuração do socket
    host = '127.0.0.1'  # Endereço do servidor (localhost)
    porta = 12345       # Porta para comunicação
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, porta))
    servidor.listen(1)
    print("Aguardando conexão do transmissor...")
    conexao, endereco = servidor.accept()
    print(f"Conexão estabelecida com: {endereco}")

    # Receber o sinal
    dados_recebidos = conexao.recv(1024).decode()
    sinal_modulado = eval(dados_recebidos)  # Convertendo de string para lista
    print(f"Sinal recebido: {sinal_modulado}")

    # Escolha da demodulação (deve estar alinhada com o transmissor)
    tipo_modulacao = input("Escolha a modulação usada (NRZ, Manchester, Bipolar): ").lower()

    if tipo_modulacao == "nrz":
        bits_demodulados = demodular_nrz(sinal_modulado)
    elif tipo_modulacao == "manchester":
        bits_demodulados = demodular_manchester(sinal_modulado)
    elif tipo_modulacao == "bipolar":
        bits_demodulados = demodular_bipolar(sinal_modulado)
    else:
        print("Demodulação inválida!")
        return

    print(f"Bits demodulados: {bits_demodulados}")

    # Correção de erros
    bits_corrigidos = hamming_decode(''.join(map(str, bits_demodulados)))
    print(f"Bits corrigidos: {bits_corrigidos}")

    # Conversão para texto
    try:
        texto_recebido = bits_para_texto(list(map(int, bits_corrigidos)))
        print(f"Texto recebido: {texto_recebido}")
    except ValueError as e:
        print(f"Erro na conversão para texto: {e}")

    conexao.close()
    servidor.close()

if __name__ == "__main__":
    receber_dados()
