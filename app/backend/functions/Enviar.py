from random import randint


def calcularErro(text, erro=0):
    text = text.replace(" ", "")
    text = text.replace("\n", "")
    text = text.replace("\t", "")
    text = [i for i in text]
    text = [int(i) for i in text]
    
    porcentagem = randint(0, 100)

    if porcentagem < int(erro):
        posicao = randint(0, text.__len__())
        text[posicao] = 1 if text[posicao] == 0 else 0 
        print("Erro na posição: ", posicao)

    return text 
    

def enviarSinal(text , erro):
    text = calcularErro(text , erro)

    return text

    #socket aqui ..................

    
   


# Teste   
#print(calcularErro("0110000 0111011 0110010 0110000 0111011 0110010"))
