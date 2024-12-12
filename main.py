from Funcao_Grafica.GeradorDeOndas import GeradorDeOndas

def main():

    ondas = GeradorDeOndas(1)

    ondas.BitStream([1,0,1,1,0])

    ondas.GerarOndaDigitais()

    ondas.SetFrequency(1)

    ondas.GerarOndaAnalogicas()   

if __name__ == '__main__':
    main()