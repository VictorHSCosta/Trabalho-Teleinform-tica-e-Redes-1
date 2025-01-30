import numpy as np  # Importa a biblioteca NumPy para cálculos numéricos eficientes.
from math import floor  # Importa a função floor para arredondamento.

class GeradorSinalDigital:
    """
    Classe responsável por gerar sinais digitais modulados usando os esquemas NRZ, Manchester e Bipolar.
    Permite configurar o fluxo de bits, os níveis de tensão e o número de pontos por bit.
    """

    def __init__(self):
        """
        Inicializa os parâmetros do gerador de sinal digital com valores padrão.
        """
        self.fluxo_bits = []  # Lista que armazenará o fluxo de bits a ser modulado
        self.tensao_minima = -1  # Valor da tensão mínima do sinal
        self.tensao_maxima = 1  # Valor da tensão máxima do sinal
        self.tamanho = 0  # Inicializa o tamanho do fluxo de bits
        self.numero_pontos = 100  # Define quantos pontos serão usados para representar cada bit
        self.tempo = 0  # Array de tempo que será atualizado com base no fluxo de bits

    # ---------------- Métodos de configuração ----------------

    def definir_fluxo_bits(self, fluxo_bits):
        """
        Define o fluxo de bits e recalcula o array de tempo correspondente.
        :param fluxo_bits: Lista de bits (0s e 1s) que serão modulados.
        """
        self.fluxo_bits = fluxo_bits
        self.tamanho = len(fluxo_bits)  # Define o tamanho do fluxo de bits
        self.tempo = np.arange(0, self.tamanho, 1 / self.numero_pontos)  # Cria o vetor de tempo

    def definir_tensao(self, tensao):
        """
        Define os valores de tensão mínima e máxima.
        :param tensao: Valor da tensão máxima (a mínima será o negativo desse valor).
        """
        self.tensao_minima = -tensao
        self.tensao_maxima = tensao

    def definir_numero_pontos(self, numero_pontos):
        """
        Define o número de pontos por bit e recalcula o array de tempo.
        :param numero_pontos: Quantidade de amostras para representar cada bit.
        """
        self.numero_pontos = numero_pontos
        self.tempo = np.arange(0, self.tamanho, 1 / self.numero_pontos)  # Atualiza o vetor de tempo

    # ---------------- Modulação NRZ (Non-Return-to-Zero) ----------------

    def gerar_nrz(self):
        """
        Gera o sinal modulado NRZ (Non-Return-to-Zero).
        No NRZ, o bit 1 é representado por um nível de tensão alto e o bit 0 por um nível de tensão baixo.
        :return: Tupla (tempo, sinal_modulado)
        """
        conteudo = 0  # Variável que armazena a tensão atual do sinal
        indice = 0  # Índice do array de tempo
        sinal = np.zeros(self.tamanho * self.numero_pontos).astype(int)  # Inicializa o array do sinal NRZ

        for i in range(self.tamanho):  # Percorre todos os bits do fluxo
            if self.fluxo_bits[i] == 1:
                conteudo = self.tensao_maxima  # Define a tensão máxima para bit 1
            else:
                conteudo = self.tensao_minima  # Define a tensão mínima para bit 0

            for j in range(self.numero_pontos):  # Preenche os pontos para representar cada bit
                sinal[indice] = conteudo
                indice += 1

        return self.tempo, sinal  # Retorna os valores do tempo e do sinal NRZ gerado

    # ---------------- Geração de Sinal de Clock ----------------

    def gerar_clock(self):
        """
        Gera um sinal de clock alternando entre os níveis de tensão.
        O clock oscila entre os níveis de tensão máxima e mínima a cada 50 amostras.
        :return: Array do sinal de clock.
        """
        sinal = np.zeros(self.tamanho * 100).astype(int)  # Inicializa o sinal de clock
        conteudo = self.tensao_maxima  # Começa com tensão máxima

        for i in range(self.tamanho * 100):
            if i % 50 == 0:  # Alterna a tensão a cada 50 pontos
                conteudo = self.tensao_maxima if conteudo == self.tensao_minima else self.tensao_minima
            sinal[i] = conteudo  # Define o valor do sinal no índice atual

        return sinal  # Retorna o sinal de clock gerado

    # ---------------- Modulação Manchester ----------------

    def gerar_manchester(self):
        """
        Gera o sinal modulado Manchester.
        No Manchester, combinamos o NRZ com o clock para criar uma transição no meio de cada bit.
        :return: Tupla (tempo, sinal_modulado)
        """
        tempo, nrz = self.gerar_nrz()  # Obtém o sinal NRZ
        clock = self.gerar_clock()  # Obtém o sinal de clock

        sinal = np.zeros(self.tamanho * 100).astype(int)  # Inicializa o sinal Manchester

        for i in range(len(nrz)):  # Percorre todos os pontos do sinal
            # XOR entre o sinal NRZ e o clock para criar a transição no meio do bit
            sinal[i] = self.tensao_minima if (nrz[i] ^ clock[i]) == 0 else self.tensao_maxima

        return tempo, sinal  # Retorna os valores do tempo e do sinal Manchester gerado

    # ---------------- Modulação Bipolar ----------------

    def gerar_bipolar(self):
        """
        Gera o sinal modulado Bipolar.
        No Bipolar, os bits 1 alternam entre tensões positiva e negativa, enquanto os bits 0 têm tensão zero.
        :return: Tupla (tempo, sinal_modulado)
        """
        sinal = np.zeros(self.tamanho * 100).astype(int)  # Inicializa o sinal Bipolar
        conteudo = self.tensao_minima  # Começa com a tensão mínima
        multiplicador = 1  # Variável para alternar a polaridade dos bits 1
        indice = 0  # Índice do array de tempo

        for i in range(self.tamanho):  # Percorre todos os bits do fluxo
            if self.fluxo_bits[i] == 1:
                # Alterna a polaridade para cada bit 1
                multiplicador = self.tensao_maxima if conteudo == self.tensao_minima else self.tensao_minima
                conteudo = multiplicador  # Atualiza o valor de tensão
            else:
                multiplicador = 0  # Para bit 0, a tensão é zero

            for j in range(100):  # Preenche os pontos para representar cada bit
                sinal[indice] = multiplicador
                indice += 1

        return self.tempo, sinal  # Retorna os valores do tempo e do sinal Bipolar gerado
