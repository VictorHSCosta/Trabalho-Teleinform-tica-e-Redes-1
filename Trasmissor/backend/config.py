import os
import shutil
from .imagens import GeradorDeOndas

Ondas = GeradorDeOndas()


def apagar_conteudo_images(caminho_pasta):
  
    # Verifica se o caminho da pasta existe
    if not os.path.exists(caminho_pasta):
        print(f"A pasta '{caminho_pasta}' não existe.")
        return

    # Remove a pasta inteira e recria uma nova vazia
    try:
        shutil.rmtree(caminho_pasta)  # Remove a pasta e todo o seu conteúdo
        os.makedirs(caminho_pasta)    # Recria a pasta vazia
        print(f"Todo o conteúdo da pasta '{caminho_pasta}' foi apagado com sucesso.")
    except Exception as e:
        print(f"Erro ao apagar o conteúdo da pasta '{caminho_pasta}': {e}")

def run(stream):
  print("Running")
  Ondas.definir_fluxo_bits(stream)
  Ondas.definir_energia(1)
  Ondas.definir_precisao(100)
  Ondas.definir_frequencias(1, 2)
  apagar_conteudo_images("static/imagens/digital/")
  Ondas.gerar_ondas_digitais()
  apagar_conteudo_images("static/imagens/analogico/")
  Ondas.gerar_ondas_analogicas()