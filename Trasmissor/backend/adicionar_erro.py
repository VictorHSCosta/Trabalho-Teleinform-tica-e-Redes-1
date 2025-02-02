import random

def adicionar_erro(bits, erro_percentual):
    """
    Introduz erros aleatórios no trem de bits com base em um percentual.
    
    Parâmetros:
    - bits (list): Lista de bits representando o quadro.
    - erro_percentual (float): Probabilidade de erro (0 a 100).
    
    Retorna:
    - list: Trem de bits com erro (se ocorrer).
    """
    # Gera um número aleatório de 0 a 100
    chance_erro = random.uniform(0, 100)

    # Inicializa a lista de índices dos bits que foram alterados
    indices_erro = []
    
    # Se a chance for menor que o erro_percentual, introduz erro
    if chance_erro < erro_percentual:
        # Define a quantidade de bits a serem alterados (1 a 3)
        num_erros = random.randint(1, 3)
        
        # Escolhe aleatoriamente quais bits serão alterados
        indices_erro = random.sample(range(len(bits)), num_erros)

        print(f"⚠ Erro inserido! Alterando {num_erros} bits nas posições: {indices_erro}")

        # Inverte os bits escolhidos
        for index in indices_erro:
            bits[index] ^= 1  # Alterna entre 0 e 1

    return [bits , indices_erro]  # Retorna o novo trem de bits (com ou sem erro)


