import numpy as np  # Importa a biblioteca NumPy para operações matemáticas eficientes.

class GeradorSinalAnalogico:
    """
    Classe responsável por gerar sinais modulados ASK, FSK e PSK com base em um fluxo de bits fornecido.
    Permite configuração de amplitude, frequência e número de pontos por bit.
    """

    def __init__(self):
        """
        Inicializa os atributos do gerador de sinais com valores padrão.
        """
        self.amplitude = 1  # Amplitude do sinal gerado
        self.frequencia = 1  # Frequência da onda senoidal para representar o bit 0
        self.frequencia2 = 2  # Frequência da onda senoidal para representar o bit 1
        self.fluxo_bits = []  # Lista vazia que armazenará o fluxo de bits a ser modulado
        self.tamanho_fluxo = 0  # Inicializa o tamanho do fluxo de bits
        self.tempo = 0  # Array de tempo que será calculado com base no fluxo de bits
        self.numero_pontos = 100  # Define quantos pontos serão usados para representar cada bit
        self.sinal_ask = []  # Inicializa um array para armazenar o sinal modulado ASK

    # ------------- Métodos para configurar os parâmetros do gerador de sinal -------------

    def definir_fluxo_bits(self, fluxo_bits):
        """
        Define o fluxo de bits e recalcula o array de tempo correspondente.
        :param fluxo_bits: Lista de bits (0s e 1s) que serão modulados.
        """
        self.fluxo_bits = fluxo_bits
        self.tamanho_fluxo = len(fluxo_bits)  # Define o tamanho do fluxo de bits
        self.tempo = np.arange(0, self.tamanho_fluxo, 1 / self.numero_pontos)  # Cria o vetor de tempo

    def definir_amplitude(self, amplitude):
        """
        Define a amplitude do sinal.
        :param amplitude: Valor da amplitude da onda senoidal.
        """
        self.amplitude = amplitude

    def definir_numero_pontos(self, numero_pontos):
        """
        Define o número de pontos por bit e recalcula o array de tempo.
        :param numero_pontos: Quantidade de amostras para representar cada bit.
        """
        self.numero_pontos = numero_pontos
        self.tempo = np.arange(0, self.tamanho_fluxo, 1 / self.numero_pontos)  # Atualiza o vetor de tempo

    def definir_frequencia(self, frequencia):
        """
        Define a frequência do sinal para representar o bit 0.
        :param frequencia: Valor da frequência do sinal.
        """
        self.frequencia = frequencia

    def definir_frequencia2(self, frequencia):
        """
        Define a frequência do sinal para representar o bit 1.
        :param frequencia: Valor da frequência do sinal.
        """
        self.frequencia2 = frequencia

    # ------------- Modulação ASK (Amplitude Shift Keying) -------------

    def gerar_ask(self):
        """
        Gera um sinal modulado ASK (modulação por chaveamento de amplitude).
        No ASK, o bit 1 é representado por uma onda senoidal e o bit 0 por ausência de sinal.
        :return: Tupla (tempo, sinal_modulado)
        """
        indice = 0  # Índice para percorrer o array de tempo
        sinal = np.zeros(self.tamanho_fluxo * self.numero_pontos).astype(float)  # Inicializa o array do sinal modulado

        for bit in self.fluxo_bits:  # Percorre todos os bits do fluxo
            if bit == 1:
                # Se o bit for 1, gera uma onda senoidal com amplitude definida
                for _ in range(self.numero_pontos):
                    sinal[indice] = self.amplitude * np.sin(2 * np.pi * self.frequencia * self.tempo[indice])
                    indice += 1
            else:
                # Se o bit for 0, o sinal será zero (ausência de onda)
                for _ in range(self.numero_pontos):
                    sinal[indice] = 0
                    indice += 1

        self.sinal_ask = sinal  # Armazena o sinal modulado
        return self.tempo, sinal  # Retorna os valores do tempo e do sinal gerado

    def obter_ask(self):
        """
        Retorna o último sinal ASK gerado.
        :return: Tupla (tempo, sinal_modulado)
        """
        return self.tempo, self.sinal_ask

    # ------------- Modulação FSK (Frequency Shift Keying) -------------

    def gerar_fsk(self):
        """
        Gera um sinal modulado FSK (modulação por chaveamento de frequência).
        No FSK, o bit 0 é representado por uma onda de uma frequência f1 e o bit 1 por uma frequência f2.
        :return: Tupla (tempo, sinal_modulado)
        """
        indice = 0
        sinal = np.zeros(self.tamanho_fluxo * self.numero_pontos).astype(float)  # Inicializa o sinal modulado

        for bit in self.fluxo_bits:  # Percorre todos os bits
            if bit == 1:
                # Se o bit for 1, usa a frequência f2
                for _ in range(self.numero_pontos):
                    sinal[indice] = self.amplitude * np.sin(2 * np.pi * self.frequencia2 * self.tempo[indice])
                    indice += 1
            else:
                # Se o bit for 0, usa a frequência f1
                for _ in range(self.numero_pontos):
                    sinal[indice] = self.amplitude * np.sin(2 * np.pi * self.frequencia * self.tempo[indice])
                    indice += 1

        return self.tempo, sinal  # Retorna os valores do tempo e do sinal gerado

    # ------------- Modulação PSK (Phase Shift Keying) -------------

    def gerar_psk(self):
        """
        Gera um sinal modulado PSK (modulação por chaveamento de fase).
        No PSK, a fase da onda é alterada dependendo do bit transmitido.
        :return: Tupla (tempo, sinal_modulado)
        """
        indice = 0
        sinal = np.zeros(self.tamanho_fluxo * self.numero_pontos).astype(float)  # Inicializa o sinal modulado

        for bit in self.fluxo_bits:  # Percorre todos os bits
            if bit == 1:
                # Se o bit for 1, mantém a fase original
                for _ in range(self.numero_pontos):
                    sinal[indice] = self.amplitude * np.sin(2 * np.pi * self.frequencia * self.tempo[indice])
                    indice += 1
            else:
                # Se o bit for 0, desloca a fase da onda em π (inverte o sinal)
                for _ in range(self.numero_pontos):
                    sinal[indice] = self.amplitude * np.sin(2 * np.pi * self.frequencia * self.tempo[indice] + np.pi)
                    indice += 1

        return self.tempo, sinal  # Retorna os valores do tempo e do sinal gerado
