import numpy as np
from math import floor

class GeradorSinalDigital:
    def __init__(self):
        # Inicialização dos parâmetros
        self.fluxo_bits = []  # Fluxo de bits a ser modulado
        self.tensao_minima = -1  # Valor mínimo de tensão
        self.tensao_maxima = 1  # Valor máximo de tensão
        self.tamanho = 0  # Tamanho do fluxo de bits
        self.numero_pontos = 100  # Número de pontos por bit
        self.tempo = 0  # Array de tempo

    # Métodos de configuração

    def definir_fluxo_bits(self, fluxo_bits):
        """
        Define o fluxo de bits e calcula o array de tempo correspondente.
        """
        self.fluxo_bits = fluxo_bits
        self.tamanho = len(fluxo_bits)
        self.tempo = np.arange(0, self.tamanho, 1 / self.numero_pontos)

    def definir_tensao(self, tensao):
        """
        Define os valores de tensão mínima e máxima.
        """
        self.tensao_minima = -tensao
        self.tensao_maxima = tensao

    def definir_numero_pontos(self, numero_pontos):
        """
        Define o número de pontos por bit e recalcula o array de tempo.
        """
        self.numero_pontos = numero_pontos
        self.tempo = np.arange(0, self.tamanho, 1 / self.numero_pontos)

    # Modulação NRZ (Non-Return-to-Zero)
    def gerar_nrz(self):
        """
        Gera o sinal modulado NRZ com base no fluxo de bits.
        """
        conteudo = 0
        indice = 0
        sinal = np.zeros(self.tamanho * self.numero_pontos).astype(int)

        for i in range(self.tamanho):
            if self.fluxo_bits[i] == 1:
                conteudo = self.tensao_maxima
            else:
                conteudo = self.tensao_minima

            for j in range(self.numero_pontos):
                sinal[indice] = conteudo
                indice += 1

        return self.tempo, sinal

    # Sinal de Clock
    def gerar_clock(self):
        """
        Gera o sinal de clock com alternância de tensão.
        """
        sinal = np.zeros(self.tamanho * 100).astype(int)
        conteudo = self.tensao_maxima

        for i in range(self.tamanho * 100):
            if i % 50 == 0:
                conteudo = self.tensao_maxima if conteudo == self.tensao_minima else self.tensao_minima
            sinal[i] = conteudo

        return sinal

    # Modulação Manchester
    def gerar_manchester(self):
        """
        Gera o sinal modulado Manchester combinando NRZ e Clock.
        """
        tempo, nrz = self.gerar_nrz()
        clock = self.gerar_clock()

        sinal = np.zeros(self.tamanho * 100).astype(int)
        for i in range(len(nrz)):
            sinal[i] = self.tensao_minima if (nrz[i] ^ clock[i]) == 0 else self.tensao_maxima

        return tempo, sinal

    # Modulação Bipolar
    def gerar_bipolar(self):
        """
        Gera o sinal modulado Bipolar com alternância de polaridade para bits 1.
        """
        sinal = np.zeros(self.tamanho * 100).astype(int)
        conteudo = self.tensao_minima
        multiplicador = 1
        indice = 0

        for i in range(self.tamanho):
            if self.fluxo_bits[i] == 1:
                multiplicador = self.tensao_maxima if conteudo == self.tensao_minima else self.tensao_minima
                conteudo = multiplicador
            else:
                multiplicador = 0

            for j in range(100):
                sinal[indice] = multiplicador
                indice += 1

        return self.tempo, sinal
