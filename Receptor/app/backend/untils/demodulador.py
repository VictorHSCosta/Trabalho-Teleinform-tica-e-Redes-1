import numpy as np

class DemoduladorSinal:
    def __init__(self):
        # Inicializa os parâmetros
        self.tensao_minima = -1
        self.tensao_maxima = 1
        self.numero_pontos = 100  # Número de pontos por bit

    def definir_tensao(self, tensao):
        """
        Define os valores de tensão mínima e máxima.
        """
        self.tensao_minima = -tensao
        self.tensao_maxima = tensao

    def definir_numero_pontos(self, numero_pontos):
        """
        Define o número de pontos por bit.
        """
        self.numero_pontos = numero_pontos

    def demodular_nrz(self, sinal):
        """
        Demodula um sinal NRZ e retorna o fluxo de bits.
        """
        bits = []
        for i in range(0, len(sinal), self.numero_pontos):
            amostra = sinal[i:i + self.numero_pontos]
            media = np.mean(amostra)  # Calcula a média dos pontos do bit
            if media > 0:
                bits.append(1)
            else:
                bits.append(0)
        return bits

    def demodular_manchester(self, sinal):
        """
        Demodula um sinal Manchester e retorna o fluxo de bits.
        """
        bits = []
        for i in range(0, len(sinal), 2 * self.numero_pontos):
            amostra_alta = sinal[i:i + self.numero_pontos]
            amostra_baixa = sinal[i + self.numero_pontos:i + 2 * self.numero_pontos]
            media_alta = np.mean(amostra_alta)
            media_baixa = np.mean(amostra_baixa)

            if media_alta > media_baixa:  # Transição alta para baixa
                bits.append(0)
            elif media_baixa > media_alta:  # Transição baixa para alta
                bits.append(1)
            else:
                raise ValueError("Erro ao demodular: padrão inválido no sinal Manchester.")
        return bits

    def demodular_bipolar(self, sinal):
        """
        Demodula um sinal Bipolar e retorna o fluxo de bits.
        """
        bits = []
        for i in range(0, len(sinal), self.numero_pontos):
            amostra = sinal[i:i + self.numero_pontos]
            media = np.mean(amostra)

            if abs(media) > 0:  # Bit 1 com alternância de polaridade
                bits.append(1)
            else:  # Bit 0 (sem polaridade)
                bits.append(0)
        return bits
