import matplotlib.pyplot as plt
from Modulacao.analogico import *
from Modulacao.digital import * 
from config import get_path


class GeradorDeOndas:

    def __init__(self,V):
        self.bit_stream = []
        self.energia = V
        self.Digital = False
        self.precisao = 100
        self.frequency = 1
        self.frequency2 = 2
        self.GeradorDeOndasDigitais = SignalGeneratorDigital()
        self.GeradorDeOndasAnalogicas = SignalGeneratorAnalogic()

    # configuracoes gets e sets

    def BitStream(self, bit_stream):
        self.bit_stream = bit_stream
        self.GeradorDeOndasDigitais.setBitStream(bit_stream)
    
    def SetEnergia(self, energia):
        self.energia = energia

    def SetPrecisao(self, precisao):
        self.precisao = precisao
    
    def SetFrequency(self, frequency):
        self.frequency = frequency
    
    def SetFrequency2(self, frequency2):
        self.frequency2 = frequency2

    # funcoes de plotagem

    def plotar_sinal(self, sinal ,title, eixo_x, eixo_y , tempo = []):
        nameFile = title

        if self.Digital: 
            path = get_path() + "/ImagensPlotadas/Digitais/" + nameFile + ".png" 
        else:
            path = get_path() + "/ImagensPlotadas/Analogicas/" + nameFile + ".png"

        plt.plot(tempo , sinal)
        plt.title(title)
        plt.xlabel(eixo_x)
        plt.ylabel(eixo_y)

        plt.savefig(path,format='png')
        plt.close()

    def GerarOndaNRZ(self):
        x , y = self.GeradorDeOndasDigitais.NRZ()
        self.Digital = True
        self.plotar_sinal(y, "Sinal NRZ", "Tempo", "Amplitude" ,x)

    def GerarOndaManchester(self):
        x , y = self.GeradorDeOndasDigitais.Manchester()
        self.Digital = True
        self.plotar_sinal(y, "Sinal Manchester", "Tempo", "Amplitude",x)

    def GerarOndaBipolar(self):
        x , y = self.GeradorDeOndasDigitais.Bipolar()
        self.Digital = True
        self.plotar_sinal(y, "Sinal Bipolar", "Tempo", "Amplitude",x)

    def SetASK(self):
        x , y = self.GeradorDeOndasAnalogicas.Ask()
        self.Digital = False
        self.plotar_sinal(y, "Sinal ASK", "Tempo", "Amplitude",x)

    def SetFSK(self):
        x , y = self.GeradorDeOndasAnalogicas.FSK()
        self.Digital = False
        self.plotar_sinal(y, "Sinal FSK", "Tempo", "Amplitude",x)

    def SetPSK(self):
        x , y = self.GeradorDeOndasAnalogicas.PSK()
        self.Digital = False
        self.plotar_sinal(y, "Sinal PSK", "Tempo", "Amplitude",x)

    def GerarOndaDigitais (self) :
        # configura a onda digital
        self.GeradorDeOndasDigitais.setV(self.energia)
        self.GeradorDeOndasDigitais.setBitStream(self.bit_stream)
        self.GeradorDeOndasDigitais.setPointsNumber(self.precisao)
        # gera as ondas digitais
        self.GerarOndaNRZ()
        self.GerarOndaManchester()
        self.GerarOndaBipolar()

    def GerarOndaAnalogicas (self) :
        # configura a onda analogica
        self.GeradorDeOndasAnalogicas.SetBitStream(self.bit_stream)
        self.GeradorDeOndasAnalogicas.SetAmplitude(self.energia)
        self.GeradorDeOndasAnalogicas.SetPointsNumber(self.precisao)
        self.GeradorDeOndasAnalogicas.SetFrequency(self.frequency)#1hz
        self.GeradorDeOndasAnalogicas.SetFrequency2(self.frequency2)#2hz
        # gera as ondas analogicas
        self.SetASK()
        self.SetFSK()
        self.SetPSK()
        
        
    