from Grafica.GeradorDeOndas import GeradorDeOndas

def main():

    ondas = GeradorDeOndas(1)

    ondas.BitStream([0,1,0,1,0,0,1,1])

    ondas.GerarOnda()

    #plotar_sinal(y, "Sinal ASK", "Tempo", "Amplitude",x,"analogico")

if __name__ == '__main__':
    main()