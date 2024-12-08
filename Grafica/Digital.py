import matplotlib.pyplot as plt
from config import get_path

def plotar_sinal( sinal ,title, eixo_x, eixo_y , tempo = [],type = "digital"):
    nameFile = title

    if type == "digital": 
        path = get_path() + "/ImagensPlotadas/Digitais/" + nameFile + ".png" 
    else:
        path = get_path() + "/ImagensPlotadas/Analogicas/" + nameFile + ".png"

    if len(tempo) == 0:
        plt.plot(sinal)
    else:
        plt.plot(tempo , sinal)
    plt.title(title)
    plt.xlabel(eixo_x)
    plt.ylabel(eixo_y)

    plt.savefig(path,format='png')
    plt.close()
    