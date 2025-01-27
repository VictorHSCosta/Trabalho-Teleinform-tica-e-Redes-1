import socket
from flask import jsonify
from app.backend.untils.demodulador import DemoduladorSinal
from app.backend.untils.correcao_de_erros import CorrecaoHamming


def iniciar_servidor():
    """
    Recebe o sinal, demodula, corrige erros e retorna o resultado.
    """
    host = '0.0.0.0'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((host, port))
        servidor.listen(1)
        print("Servidor aguardando conexão...")

        conn, addr = servidor.accept()
        with conn:
            print(f"Conexão estabelecida com {addr}")
            dados = conn.recv(1024).decode('utf-8')
            print(f"Dados recebidos: {dados}")

            try:
                # Extrai o tipo e o sinal do dado recebido
                tipo, sinal_str = dados.split(':')
                sinal = [float(valor) for valor in sinal_str.split(',') if valor.strip()]

                # Processa e corrige o sinal
                fluxo_destacado, fluxo_corrigido = processar_e_corrigir_sinal(sinal, tipo)

                # Retorna os resultados como dicionário
                return {
                    "fluxo_destacado": fluxo_destacado,
                    "fluxo_corrigido": "".join(map(str, fluxo_corrigido))
                }
            except Exception as e:
                print(f"Erro ao processar os dados recebidos: {e}")
                return {"erro": f"Erro ao processar os dados: {e}"}


def processar_e_corrigir_sinal(sinal, tipo):
    """
    Processa, demodula e corrige erros no sinal recebido.
    """
    demodulador = DemoduladorSinal()
    demodulador.definir_tensao(1)  # Define a amplitude padrão
    demodulador.definir_numero_pontos(100)  # Define o número de pontos por bit

    try:
        # Seleciona o método de demodulação com base no tipo
        if tipo == "NRZ":
            bits_demodulados = demodulador.demodular_nrz(sinal)
        elif tipo == "Manchester":
            bits_demodulados = demodulador.demodular_manchester(sinal)
        elif tipo == "Bipolar":
            bits_demodulados = demodulador.demodular_bipolar(sinal)
        else:
            raise ValueError("Tipo de modulação inválido.")

        print(f"Bits demodulados: {bits_demodulados}")

        # Corrige erros usando o Código de Hamming
        sindrome, bits_corrigidos = CorrecaoHamming.corrigir_erro(bits_demodulados)
        bits_destacados = CorrecaoHamming.destacar_erros(bits_demodulados, bits_corrigidos)

        print(f"Bits corrigidos: {bits_corrigidos}")
        print(f"Fluxo destacado: {bits_destacados}")

        return bits_destacados, bits_corrigidos
    except Exception as e:
        print(f"Erro ao processar o sinal: {e}")
        raise
