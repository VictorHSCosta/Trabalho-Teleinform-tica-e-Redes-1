import socket
import json
from .deteccao_de_erros import adicionar_paridade, detectar_erros_quadros, verificar_paridade, adicionar_crc32, verificar_crc32
from .adicionar_erro import adicionar_erro
from .conversores import bits_para_decimal, texto_para_bits, bits_para_texto ,decimal_para_bits
from .hamming import aplicar_hamming_quadros ,corrigir_erros_quadros 
from .modulador import modular_quadros
from .enquadramento import enquadramento_contagem_caracteres, enquadramento_insercao_bytes ,desenquadramento_contagem_caracteres, desenquadramento_insercao_bytes


def enviar_dados(HOST ,texto ,tipo_modulacao,porcentagem_erro, enquadramento, deteccao_erro):
    # Configuração do cliente socket
  # O usuário pode digitar o IP do servidor Flask
    HOST = '172.29.45.194'
    PORTA = 12345  # Mesma porta do servidor

    # Criar o socket
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORTA))

    # Trasforma o texto em bits
    bits = texto_para_bits(texto)

    #É necessario trasformar a mensagem com erro em string para poder ser enviada
    mensagem_com_erro = bits_para_texto(bits)
    print(f"Mensagem sem erro: {texto}")

    #enquadramento da mensagem
    quadro = []
    quadroBits = []
    if enquadramento == "Contagem de bit":
        quadro = enquadramento_contagem_caracteres(mensagem_com_erro)
    elif enquadramento == "Inserção de bytes":
        quadro =enquadramento_insercao_bytes(mensagem_com_erro)
    else:
        print("Método de enquadramento inválido. Escolha 'Contagem de Caracteres' ou 'Inserção de Bytes'.")
        return
    quadroBits = decimal_para_bits(quadro[0])
    print(f"Quadro: {quadro}")
    print("--------------------")

    ##colocamos o codigo de hamming para funcionar
    print("Aplicando codigo de hamming")
    codigo_hamming = aplicar_hamming_quadros(quadro)[0]

    ## Adicionamos erro no codigo de hamming
    codigo_hamming = decimal_para_bits(codigo_hamming)
    erroHamming = adicionar_erro(codigo_hamming, porcentagem_erro)
    codigo_hamming = erroHamming[0]
    codigo_hamming = bits_para_decimal(codigo_hamming)
    codigo_hamming = [codigo_hamming]

    #teste para verificar se o codigo de hamming esta funcionando
    #corrigir erros
    desenquadramento = corrigir_erros_quadros(codigo_hamming)
    desenquadramento = desenquadramento_contagem_caracteres(desenquadramento) if enquadramento == "Contagem de bit" else desenquadramento_insercao_bytes(desenquadramento)
    print(f"Mensagem que vai chegar: {desenquadramento}")
    print("--------------------")


    #bit de paridade 
    print("Adicionando bit de paridade")
    # primeiro convertemos o quadro em bits
    bitParidade = adicionar_paridade(quadroBits)
    erroParidade = adicionar_erro(bitParidade, porcentagem_erro)
    bitParidade = erroParidade[0]
    print(f"Esta correto o bit de paridade: {verificar_paridade(bitParidade)}")
    print("--------------------")

    #crc32

    print("Adicionando crc32")
    crc32 = adicionar_crc32(quadroBits)
    erroCrc32 = adicionar_erro(crc32, porcentagem_erro)
    crc32 = erroCrc32[0]
    print(f"Esta correto o crc32: {verificar_crc32(crc32)}")

    sinal_modulado = []

    if deteccao_erro == "Bit de paridade":
        sinal_modulado = bitParidade
    elif deteccao_erro == "CRC":
        sinal_modulado = crc32
    elif deteccao_erro == "Código de Hamming":
        sinal_modulado = codigo_hamming
    else:
        print("Método de detecção inválido. Escolha 'Paridade' ou 'CRC-32'.")
        return
    

    # Criar JSON com os dados
    dados = {
        "sinal_modulado": sinal_modulado,
        "metodo_enquadramento": enquadramento,
        "tipo_modulacao": tipo_modulacao,
        "deteccao_erro": deteccao_erro,
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
    #enviar_dados()
    enviar_dados("127.0.0.1" ,"Hello, World! 😊" ,"NRZ",100, "Contagem de bit", "")

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

# teste


