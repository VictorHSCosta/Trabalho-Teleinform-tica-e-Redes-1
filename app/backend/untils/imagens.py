import matplotlib.pyplot as plt
from .digital import GeradorSinalDigital
from .analogico import GeradorSinalAnalogico

class GeradorDeOndas:

    def __init__(self):
        # Inicialização dos parâmetros
        self.fluxo_bits = []  # Fluxo de bits a ser processado
        self.energia = 1  # Energia do sinal
        self.digital = False  # Define se o sinal é digital ou analógico
        self.precisao = 100  # Precisão (número de pontos por bit)
        self.frequencia = 1  # Frequência para o sinal analógico (bit 0)
        self.frequencia2 = 2  # Frequência para o sinal analógico (bit 1)
        self.gerador_digital = GeradorSinalDigital()
        self.gerador_analogico = GeradorSinalAnalogico()

    # Configurações

    def definir_fluxo_bits(self, fluxo_bits):
        """
        Define o fluxo de bits a ser modulado.
        """
        self.fluxo_bits = fluxo_bits
        self.gerador_digital.definir_fluxo_bits(fluxo_bits)

    def definir_energia(self, energia):
        """
        Define a energia do sinal.
        """
        self.energia = energia

    def definir_precisao(self, precisao):
        """
        Define o número de pontos por bit (precisão).
        """
        self.precisao = precisao

    def definir_frequencias(self, frequencia, frequencia2):
        """
        Define as frequências para os sinais analógicos.
        """
        self.frequencia = frequencia
        self.frequencia2 = frequencia2

    # Funções de plotagem

    def plotar_sinal(self, sinal, titulo, eixo_x, eixo_y, tempo=[]):
        """
        Plota o sinal gerado e salva como imagem.
        """
        nome_arquivo = titulo

        if self.digital:
            caminho = f"app/static/images/digital/{nome_arquivo}.png" 
        else:
            caminho = f"app/static/images/analogico/{nome_arquivo}.png"

        plt.plot(tempo, sinal)
        plt.title(titulo)
        plt.xlabel(eixo_x)
        plt.ylabel(eixo_y)


        print(caminho)
        plt.savefig(caminho, format='png')
        plt.close()

    # Geração de sinais digitais

    def gerar_onda_nrz(self):
        tempo, sinal = self.gerador_digital.gerar_nrz()
        self.digital = True
        self.plotar_sinal(sinal, "Sinal NRZ", "Tempo", "Amplitude", tempo)

    def gerar_onda_manchester(self):
        tempo, sinal = self.gerador_digital.gerar_manchester()
        self.digital = True
        self.plotar_sinal(sinal, "Sinal Manchester", "Tempo", "Amplitude", tempo)

    def gerar_onda_bipolar(self):
        tempo, sinal = self.gerador_digital.gerar_bipolar()
        self.digital = True
        self.plotar_sinal(sinal, "Sinal Bipolar", "Tempo", "Amplitude", tempo)

    # Geração de sinais analógicos

    def gerar_sinal_ask(self):
        tempo, sinal = self.gerador_analogico.gerar_ask()
        self.digital = False
        self.plotar_sinal(sinal, "Sinal ASK", "Tempo", "Amplitude", tempo)

    def gerar_sinal_fsk(self):
        tempo, sinal = self.gerador_analogico.gerar_fsk()
        self.digital = False
        self.plotar_sinal(sinal, "Sinal FSK", "Tempo", "Amplitude", tempo)

    def gerar_sinal_psk(self):
        tempo, sinal = self.gerador_analogico.gerar_psk()
        self.digital = False
        self.plotar_sinal(sinal, "Sinal PSK", "Tempo", "Amplitude", tempo)

    # Geração combinada de ondas

    def gerar_ondas_digitais(self):
        """
        Configura e gera todas as ondas digitais.
        """
        self.gerador_digital.definir_tensao(self.energia)
        self.gerador_digital.definir_fluxo_bits(self.fluxo_bits)
        self.gerador_digital.definir_numero_pontos(self.precisao)

        self.gerar_onda_nrz()
        self.gerar_onda_manchester()
        self.gerar_onda_bipolar()

    def gerar_ondas_analogicas(self):
        """
        Configura e gera todas as ondas analógicas.
        """
        self.gerador_analogico.definir_fluxo_bits(self.fluxo_bits)
        self.gerador_analogico.definir_amplitude(self.energia)
        self.gerador_analogico.definir_numero_pontos(self.precisao)
        self.gerador_analogico.definir_frequencia(self.frequencia)
        self.gerador_analogico.definir_frequencia2(self.frequencia2)

        self.gerar_sinal_ask()
        self.gerar_sinal_fsk()
        self.gerar_sinal_psk()
