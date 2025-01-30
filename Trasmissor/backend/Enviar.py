import socket
import json
from .adicionar_erro import adicionar_erro
from .conversores import texto_para_bits
from .hamming import hamming_encode
from .modulador import modular_nrz, modular_manchester, modular_bipolar


def enviar_dados(HOST ,texto ,tipo_modulacao,porcentagem_erro, enquadramento, deteccao_erro):
    # Configuração do cliente socket
  # O usuário pode digitar o IP do servidor Flask
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
    porcentagem_erro = float(porcentagem_erro)
    if porcentagem_erro < 0 or porcentagem_erro > 100:
        print("Porcentagem de erro inválida!")
        return
    bits_com_erro = adicionar_erro(list(map(int, bits_codificados)), porcentagem_erro)
    print(f"Bits com erro: {bits_com_erro}")

    # Escolha da modulação
    tipo_modulacao = tipo_modulacao.lower()
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

#Uma forma de aplicar as novas funções no transmissor (enquadramento.py,hamming.py,modulador.py)

#def transmitir(mensagem, metodo_enquadramento, metodo_modulacao):
    #"""Faz todo o processo de transmissão: Enquadramento -> Hamming -> Modulação -> Envio."""
    
    # 1️⃣ Enquadramento
   # if metodo_enquadramento == "Contagem de Caracteres":
       # quadros = enquadramento_contagem_caracteres(mensagem)
    #elif metodo_enquadramento == "Inserção de Bytes":
        #quadros = enquadramento_insercao_bytes(mensagem)
   # else:
        #raise ValueError("Método de enquadramento inválido. Escolha 'Contagem de Caracteres' ou 'Inserção de Bytes'.")
    
    

    # 2️⃣ Aplicação do Código de Hamming
    #quadros_codificados = aplicar_hamming_quadros(quadros)

    # 3️⃣ Modulação
    #sinais_modulados = modular_quadros(quadros_codificados, metodo_modulacao)

    # 4️⃣ Simulação de Transmissão
    #print(f"\n🔹 Mensagem Transmitida ({metodo_modulacao}):")
    #for i, sinal in enumerate(sinais_modulados):
        #print(f"Quadro {i+1}: {sinal}")

    #return sinais_modulados  # Retorna o sinal modulado para simular o envio