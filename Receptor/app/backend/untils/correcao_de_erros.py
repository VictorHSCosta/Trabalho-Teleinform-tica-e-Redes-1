class CorrecaoHamming:
    @staticmethod
    def corrigir_erro(bits):
        """
        Corrige erros no trem de bits usando o Código de Hamming.
        Retorna o índice do bit com erro (se houver) e o fluxo de bits corrigido.
        """
        # Converte o fluxo de bits em uma lista para manipulação
        bits = list(map(int, bits))
        n = len(bits)

        # Localiza bits de paridade
        posicoes_paridade = [2**i for i in range(n) if 2**i - 1 < n]

        # Calcula os valores dos bits de paridade no fluxo recebido
        sindrome = 0
        for pos in posicoes_paridade:
            valor_paridade = 0
            for i in range(pos - 1, n, pos * 2):
                valor_paridade ^= sum(bits[i:i + pos])
            if valor_paridade % 2 != 0:
                sindrome += pos

        # Se o síndrome for diferente de 0, há erro
        if sindrome > 0 and sindrome <= n:
            print(f"Erro encontrado na posição: {sindrome}")
            bits[sindrome - 1] ^= 1  # Corrige o erro invertendo o bit
        else:
            print("Nenhum erro encontrado.")

        return sindrome, bits

    @staticmethod
    def destacar_erros(bits_original, bits_corrigidos):
        """
        Destaca os bits alterados na correção, retornando o fluxo com erros destacados.
        """
        fluxo_destacado = [
            f"<span style='color: red;'>{corrigido}</span>" if original != corrigido else f"{corrigido}"
            for original, corrigido in zip(bits_original, bits_corrigidos)
        ]
        return "".join(fluxo_destacado)
