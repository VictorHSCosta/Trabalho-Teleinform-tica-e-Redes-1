import socket
import json
from .deteccao_de_erros import adicionar_paridade, detectar_erros_quadros, verificar_paridade, adicionar_crc32, verificar_crc32
from .adicionar_erro import adicionar_erro
from .conversores import bits_para_decimal, texto_para_bits, bits_para_texto ,decimal_para_bits
from .hamming import aplicar_hamming_quadros ,corrigir_erros_quadros 
from .modulador import modular_quadros
from .enquadramento import enquadramento_contagem_caracteres, enquadramento_insercao_bytes ,desenquadramento_contagem_caracteres, desenquadramento_insercao_bytes
from .config import run
from .bytecode import get_bytecode

def GerarGrafico(stream):
    get_bytecode(stream)

def arrumar_codigo(sinal , tipo_enquadramento, deteccao_erro):
    """Função que recebe o sinal modulado e o tipo de modulação e retorna o texto recebido"""

    texto = ""
    desenquadramento = []
    
    #Desenquadramento usando hamming
    if deteccao_erro == "Código de Hamming":
        desenquadramento = corrigir_erros_quadros(sinal)
        desenquadramento =  desenquadramento_contagem_caracteres(desenquadramento) if tipo_enquadramento == "Contagem de bit" else desenquadramento_insercao_bytes(desenquadramento)
        #gera as imagens
        GerarGrafico(desenquadramento)
        texto = desenquadramento
        desenquadramento = texto_para_bits(desenquadramento)
    elif deteccao_erro == "CRC":
        verificar = verificar_crc32(sinal)
        print(f"verificar: {verificar}")
        if verificar == True:
            desenquadramento =  desenquadramento_contagem_caracteres(sinal) if tipo_enquadramento == "Contagem de bit" else desenquadramento_insercao_bytes(sinal)
            print(f"Mensagem que vai chegar: {desenquadramento}")
            texto = "desenquadramento"
        else:
            print("Erro no CRC")
            desenquadramento = []
            texto = "Erro no CRC"
    elif deteccao_erro == "Bit de paridade":
        desenquadramento = verificar_paridade(sinal)
        if desenquadramento == True:
            desenquadramento =  desenquadramento_contagem_caracteres(sinal) if tipo_enquadramento == "Contagem de bit" else desenquadramento_insercao_bytes(sinal)
            print(f"Mensagem que vai chegar: {desenquadramento}")
            texto = "desenquadramento"
        else:
            print("Erro no Bit de paridade")
            desenquadramento = []
            texto = "Erro no Bit de paridade"

    print(f"Texto recebido: {texto} opa")
    print(f"Desenquadramento: {desenquadramento}")
        
    
    return [texto, desenquadramento]