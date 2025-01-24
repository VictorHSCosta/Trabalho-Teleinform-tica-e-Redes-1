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
  apagar_conteudo_images("app/static/images/digital/")
  Ondas.gerar_ondas_digitais()
  apagar_conteudo_images("app/static/images/analogico/")
  Ondas.gerar_ondas_analogicas()

def configurar(energia , precisao, frequencia1, frequencia2):
  Ondas.definir_energia(int(energia))
  Ondas.definir_precisao(int(precisao))
  Ondas.definir_frequencias(int(frequencia1), int(frequencia2))
  print("Configuração realizada com sucesso")
  return "Configuração realizada com sucesso"

def get_config():
    energia = Ondas.energia
    precisao = Ondas.precisao
    frequencia1 = Ondas.frequencia1
    frequencia2 = Ondas.frequencia2
    return {"energia": energia, "precisao": precisao, "frequencia1": frequencia1, "frequencia2": frequencia2}

