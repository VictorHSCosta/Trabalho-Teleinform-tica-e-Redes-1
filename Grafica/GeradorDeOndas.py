import matplotlib.pyplot as plt
from Modulacao.analogico import *
from Modulacao.digital import * 
from config import get_path


class GeradorDeOndas:

    def __init__(self,V):
        self.bit_stream = []
        self.Vmax = V
        self.Vmin = -V
        self.Digital = False
        self.GeradorDeOndasDigitais = SignalGenerator(self.bit_stream,V)

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

    def BitStream(self, bit_stream):
        self.bit_stream = bit_stream
        self.GeradorDeOndasDigitais.setBitStream(bit_stream)

    def GerarOnda(self) :
        self.GerarOndaNRZ()
        self.GerarOndaManchester()
        self.GerarOndaBipolar()

        
    