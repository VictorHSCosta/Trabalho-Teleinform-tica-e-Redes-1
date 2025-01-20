from random import randint


def calcularErro(text, erro=0):
    text = text.replace(" ", "")
    text = text.replace("\n", "")
    text = text.replace("\t", "")
    text = [i for i in text]
    text = [int(i) for i in text]

    print("Erro: ", erro)
    print("Texto sem erro: ", text)
    
    porcentagem = randint(0, 100)
    if porcentagem < erro:
        posicao = randint(0, text.__len__())
        text[posicao] = 1 if text[posicao] == 0 else 0 
        print("Erro na posição: ", posicao)

    print("Texto com erro: ", text)

    return text 

def enviarSinal(text , erro):
    text = calcularErro(text , erro)

    #socket aqui ..................

    
   


# Teste   
#print(calcularErro("0110000 0111011 0110010 0110000 0111011 0110010"))
