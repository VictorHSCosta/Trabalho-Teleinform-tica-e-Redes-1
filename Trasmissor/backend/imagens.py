import matplotlib  # Importa a biblioteca Matplotlib para gerar gráficos
from .analogico import GeradorSinalAnalogico  # Importa a classe para geração de sinais analógicos
from .digital import GeradorSinalDigital  # Importa a classe para geração de sinais digitais
matplotlib.use('Agg')  # Define o backend como 'Agg' (modo não interativo, ideal para servidores)
import matplotlib.pyplot as plt  # Importa a biblioteca de plotagem
from threading import Lock  # Importa Lock para garantir sincronização de threads
import os  # Biblioteca para manipulação de arquivos e diretórios
import gc  # Biblioteca para gerenciamento de memória

# Cria um Lock para evitar que múltiplas threads plotem simultaneamente
plot_lock = Lock()

class GeradorDeOndas:
    """
    Classe responsável por gerar sinais digitais e analógicos e plotá-los como imagens.
    Permite configuração de fluxo de bits, energia, precisão e frequência dos sinais.
    """

    def __init__(self):
        """
        Inicializa os parâmetros do gerador de ondas com valores padrão.
        """
        self.fluxo_bits = []  # Lista que armazenará o fluxo de bits
        self.energia = 1  # Define a energia do sinal (usada como amplitude)
        self.digital = False  # Indica se o sinal gerado é digital ou analógico
        self.precisao = 100  # Define a precisão, ou seja, o número de pontos por bit
        self.frequencia = 1  # Frequência para o sinal analógico (bit 0)
        self.frequencia2 = 2  # Frequência para o sinal analógico (bit 1)

        # Inicializa os geradores de sinal digital e analógico
        self.gerador_digital = GeradorSinalDigital()
        self.gerador_analogico = GeradorSinalAnalogico()

    # ---------------- Configurações dos parâmetros ----------------

    def definir_fluxo_bits(self, fluxo_bits):
        """
        Define o fluxo de bits a ser modulado e repassa a configuração ao gerador digital.
        :param fluxo_bits: Lista de bits (0s e 1s).
        """
        self.fluxo_bits = fluxo_bits
        self.gerador_digital.definir_fluxo_bits(fluxo_bits)

    def definir_energia(self, energia):
        """
        Define a energia do sinal (utilizada como amplitude).
        :param energia: Valor da amplitude do sinal.
        """
        self.energia = energia

    def definir_precisao(self, precisao):
        """
        Define o número de pontos por bit (precisão).
        :param precisao: Quantidade de amostras por bit.
        """
        self.precisao = precisao

    def definir_frequencias(self, frequencia, frequencia2):
        """
        Define as frequências utilizadas nos sinais analógicos.
        :param frequencia: Frequência para o bit 0.
        :param frequencia2: Frequência para o bit 1.
        """
        self.frequencia = frequencia
        self.frequencia2 = frequencia2

    # ---------------- Funções de Plotagem ----------------

    def plotar_sinal(self, sinal, titulo, eixo_x, eixo_y, tempo=[]):
        """
        Gera um gráfico do sinal modulado e salva como uma imagem.
        :param sinal: Lista de valores do sinal modulado.
        :param titulo: Nome do arquivo e título do gráfico.
        :param eixo_x: Rótulo do eixo X.
        :param eixo_y: Rótulo do eixo Y.
        :param tempo: Lista de valores do tempo correspondente ao sinal.
        """
        nome_arquivo = titulo  # Define o nome do arquivo com base no título

        # Define o diretório onde a imagem será salva com base no tipo de sinal (digital ou analógico)
        if self.digital:
            caminho_dir = "static/imagens/digital"
            caminho = f"{caminho_dir}/{nome_arquivo}.png"
        else:
            caminho_dir = "static/imagens/analogico"
            caminho = f"{caminho_dir}/{nome_arquivo}.png"

        # Cria o diretório caso ele não exista
        os.makedirs(caminho_dir, exist_ok=True)

        # Usa o Lock para evitar conflitos entre múltiplas threads gerando gráficos
        with plot_lock:
            plt.plot(tempo, sinal)  # Plota o sinal no gráfico
            plt.title(titulo)  # Define o título do gráfico
            plt.xlabel(eixo_x)  # Define o nome do eixo X
            plt.ylabel(eixo_y)  # Define o nome do eixo Y

            print(caminho)  # Imprime o caminho do arquivo gerado
            plt.savefig(caminho, format='png')  # Salva a imagem no formato PNG
            plt.close()  # Fecha a figura para evitar sobrecarga na memória
            gc.collect()  # Libera memória manualmente

    # ---------------- Geração de Sinais Digitais ----------------

    def gerar_onda_nrz(self):
        """
        Gera e plota um sinal modulado no formato NRZ (Non-Return-to-Zero).
        """
        tempo, sinal = self.gerador_digital.gerar_nrz()
        self.digital = True
        self.plotar_sinal(sinal, "Sinal NRZ", "Tempo", "Amplitude", tempo)

    def gerar_onda_manchester(self):
        """
        Gera e plota um sinal modulado no formato Manchester.
        """
        tempo, sinal = self.gerador_digital.gerar_manchester()
        self.digital = True
        self.plotar_sinal(sinal, "Sinal Manchester", "Tempo", "Amplitude", tempo)

    def gerar_onda_bipolar(self):
        """
        Gera e plota um sinal modulado no formato Bipolar.
        """
        tempo, sinal = self.gerador_digital.gerar_bipolar()
        self.digital = True
        self.plotar_sinal(sinal, "Sinal Bipolar", "Tempo", "Amplitude", tempo)

    # ---------------- Geração de Sinais Analógicos ----------------

    def gerar_sinal_ask(self):
        """
        Gera e plota um sinal modulado no formato ASK (Amplitude Shift Keying).
        """
        tempo, sinal = self.gerador_analogico.gerar_ask()
        self.digital = False
        self.plotar_sinal(sinal, "Sinal ASK", "Tempo", "Amplitude", tempo)

    def gerar_sinal_fsk(self):
        """
        Gera e plota um sinal modulado no formato FSK (Frequency Shift Keying).
        """
        tempo, sinal = self.gerador_analogico.gerar_fsk()
        self.digital = False
        self.plotar_sinal(sinal, "Sinal FSK", "Tempo", "Amplitude", tempo)

    def gerar_sinal_psk(self):
        """
        Gera e plota um sinal modulado no formato PSK (Phase Shift Keying).
        """
        tempo, sinal = self.gerador_analogico.gerar_psk()
        self.digital = False
        self.plotar_sinal(sinal, "Sinal PSK", "Tempo", "Amplitude", tempo)

    # ---------------- Geração Combinada de Ondas ----------------

    def gerar_ondas_digitais(self):
        """
        Configura os parâmetros e gera todos os sinais digitais.
        """
        self.gerador_digital.definir_tensao(self.energia)  # Define a amplitude/tensão do sinal
        self.gerador_digital.definir_fluxo_bits(self.fluxo_bits)  # Define os bits a serem transmitidos
        self.gerador_digital.definir_numero_pontos(self.precisao)  # Define a precisão dos sinais

        self.gerar_onda_nrz()
        self.gerar_onda_manchester()
        self.gerar_onda_bipolar()

    def gerar_ondas_analogicas(self):
        """
        Configura os parâmetros e gera todos os sinais analógicos.
        """
        self.gerador_analogico.definir_fluxo_bits(self.fluxo_bits)
        self.gerador_analogico.definir_amplitude(self.energia)
        self.gerador_analogico.definir_numero_pontos(self.precisao)
        self.gerador_analogico.definir_frequencia(self.frequencia)
        self.gerador_analogico.definir_frequencia2(self.frequencia2)

        self.gerar_sinal_ask()
        self.gerar_sinal_fsk()
        self.gerar_sinal_psk()
