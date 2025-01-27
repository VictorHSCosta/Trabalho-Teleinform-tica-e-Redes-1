import numpy as np

class GeradorSinalAnalogico:
    def __init__(self):
        # Configurações iniciais
        self.amplitude = 1  # Amplitude do sinal
        self.frequencia = 1  # Frequência do sinal para bit 0
        self.frequencia2 = 2  # Frequência do sinal para bit 1
        self.fluxo_bits = []  # Fluxo de bits a ser modulado
        self.tamanho_fluxo = 0  # Tamanho do fluxo de bits
        self.tempo = 0  # Array de tempo
        self.numero_pontos = 100  # Número de pontos por bit
        self.sinal_ask = []  # Sinal modulado ASK

    # Métodos para configurar os parâmetros do gerador de sinal
    def definir_fluxo_bits(self, fluxo_bits):
        """
        Define o fluxo de bits e calcula o array de tempo correspondente.
        """
        self.fluxo_bits = fluxo_bits
        self.tamanho_fluxo = len(fluxo_bits)
        self.tempo = np.arange(0, self.tamanho_fluxo, 1 / self.numero_pontos)

    def definir_amplitude(self, amplitude):
        """
        Define a amplitude do sinal.
        """
        self.amplitude = amplitude

    def definir_numero_pontos(self, numero_pontos):
        """
        Define o número de pontos por bit e recalcula o array de tempo.
        """
        self.numero_pontos = numero_pontos
        self.tempo = np.arange(0, self.tamanho_fluxo, 1 / self.numero_pontos)

    def definir_frequencia(self, frequencia):
        """
        Define a frequência do sinal para o bit 0.
        """
        self.frequencia = frequencia

    def definir_frequencia2(self, frequencia):
        """
        Define a frequência do sinal para o bit 1.
        """
        self.frequencia2 = frequencia

    # Modulação ASK (Amplitude Shift Keying)
    def gerar_ask(self):
        """
        Gera o sinal modulado ASK baseado no fluxo de bits.
        """
        indice = 0
        sinal = np.zeros(self.tamanho_fluxo * self.numero_pontos).astype(float)

        for bit in self.fluxo_bits:
            if bit == 1:
                for _ in range(self.numero_pontos):
                    sinal[indice] = self.amplitude * np.sin(2 * np.pi * self.frequencia * self.tempo[indice])
                    indice += 1
            else:
                for _ in range(self.numero_pontos):
                    sinal[indice] = 0
                    indice += 1

        self.sinal_ask = sinal
        return self.tempo, sinal

    def obter_ask(self):
        """
        Retorna o sinal modulado ASK gerado.
        """
        return self.tempo, self.sinal_ask

    # Modulação FSK (Frequency Shift Keying)
    def gerar_fsk(self):
        """
        Gera o sinal modulado FSK baseado no fluxo de bits.
        """
        indice = 0
        sinal = np.zeros(self.tamanho_fluxo * self.numero_pontos).astype(float)

        for bit in self.fluxo_bits:
            if bit == 1:
                for _ in range(self.numero_pontos):
                    sinal[indice] = self.amplitude * np.sin(2 * np.pi * self.frequencia2 * self.tempo[indice])
                    indice += 1
            else:
                for _ in range(self.numero_pontos):
                    sinal[indice] = self.amplitude * np.sin(2 * np.pi * self.frequencia * self.tempo[indice])
                    indice += 1

        return self.tempo, sinal

    # Modulação PSK (Phase Shift Keying)
    def gerar_psk(self):
        """
        Gera o sinal modulado PSK baseado no fluxo de bits.
        """
        indice = 0
        sinal = np.zeros(self.tamanho_fluxo * self.numero_pontos).astype(float)

        for bit in self.fluxo_bits:
            if bit == 1:
                for _ in range(self.numero_pontos):
                    sinal[indice] = self.amplitude * np.sin(2 * np.pi * self.frequencia * self.tempo[indice])
                    indice += 1
            else:
                for _ in range(self.numero_pontos):
                    sinal[indice] = self.amplitude * np.sin(2 * np.pi * self.frequencia * self.tempo[indice] + np.pi)
                    indice += 1

        return self.tempo, sinal
