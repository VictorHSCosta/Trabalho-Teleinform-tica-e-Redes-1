from Modulacao.digital import * 
from Grafica.Digital import *

def main():
    
    x , y = NRZ([0,1,0,1,0,0,1,1])

    plotar_sinal(y, "Sinal NRZ", "Tempo", "Amplitude" ,x)

    x = Clock(8)

    plotar_sinal( x, "Clock", "Tempo", "Amplitude")

    x , y = Manchester([0,1,0,1,0,0,1,1])

    plotar_sinal(y, "Sinal Manchester", "Tempo", "Amplitude",x)

    x,y = Bipolar([0,1,0,1,0,0,1,1])

    plotar_sinal(y, "Sinal Bipolar", "Tempo", "Amplitude",x)

if __name__ == '__main__':
    main()