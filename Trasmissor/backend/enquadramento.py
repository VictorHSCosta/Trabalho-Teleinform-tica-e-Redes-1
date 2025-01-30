def dividir_mensagem_em_blocos(mensagem_binaria, tamanho_bloco=26):
    """Divide a mensagem binária em blocos de tamanho fixo."""
    blocos = [mensagem_binaria[i:i + tamanho_bloco] for i in range(0, len(mensagem_binaria), tamanho_bloco)]
    
    if len(blocos[-1]) < tamanho_bloco:
        blocos[-1] += [0] * (tamanho_bloco - len(blocos[-1]))

    return blocos

def enquadramento_contagem_caracteres(mensagem: str) -> list:
    """Enquadra a mensagem usando contagem de caracteres com quadros fixos."""
    mensagem_bytes = list(mensagem.encode('utf-8'))
    
    blocos = dividir_mensagem_em_blocos(mensagem_bytes, 25)  # 1 byte para tamanho + 25 de dados
    
    quadros = []
    for bloco in blocos:
        tamanho = len(bloco)  # Define o primeiro byte como tamanho
        quadro = [tamanho] + bloco + [0] * (25 - len(bloco))  # Preenche com zeros se necessário
        quadros.append(quadro)

    return quadros

def enquadramento_insercao_bytes(mensagem: str) -> list:
    """Enquadra a mensagem usando inserção de bytes com quadros fixos."""
    FLAG = 0x7E
    ESCAPE = 0x7D
    
    mensagem_bytes = list(mensagem.encode('utf-8'))
    mensagem_enquadrada = [FLAG]

    for byte in mensagem_bytes:
        if byte in [FLAG, ESCAPE]:
            mensagem_enquadrada.append(ESCAPE)
            mensagem_enquadrada.append(byte ^ 0x20)
        else:
            mensagem_enquadrada.append(byte)
    
    mensagem_enquadrada.append(FLAG)

    blocos = dividir_mensagem_em_blocos(mensagem_enquadrada, 26)
    
    return blocos

#Vou colocar a parte de desenquadrar aqui junto, mas da pra separar os dois, porque uma parte é so no transmissor 
#e outra apenas no receptor.

def desenquadramento_contagem_caracteres(quadros):
    """Desenquadra os quadros usando contagem de caracteres."""
    mensagem_bytes = []
    for quadro in quadros:
        tamanho = quadro[0]  # Primeiro byte contém o tamanho
        mensagem_bytes.extend(quadro[1:1 + tamanho])  # Recupera os caracteres reais
    
    return bytes(mensagem_bytes).decode('utf-8')

def desenquadramento_insercao_bytes(quadros):
    """Desenquadra os quadros usando inserção de bytes."""
    FLAG = 0x7E
    ESCAPE = 0x7D
    
    mensagem_bytes = []
    escape_next = False

    for quadro in quadros:
        for byte in quadro:
            if escape_next:
                mensagem_bytes.append(byte ^ 0x20)  # Remove a operação XOR do escape
                escape_next = False
            elif byte == ESCAPE:
                escape_next = True
            elif byte != FLAG:
                mensagem_bytes.append(byte)  # Adiciona apenas os bytes válidos
    
    return bytes(mensagem_bytes).decode('utf-8')

def desenquadrar_quadros(quadros, metodo):
    """Aplica o método correto de desenquadramento."""
    if metodo == "Contagem de Caracteres":
        return desenquadramento_contagem_caracteres(quadros)
    elif metodo == "Inserção de Bytes":
        return desenquadramento_insercao_bytes(quadros)
    else:
        raise ValueError("Método de desenquadramento inválido.")