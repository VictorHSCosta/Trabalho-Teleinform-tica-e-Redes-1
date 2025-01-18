from .imagens import GeradorDeOndas

Ondas = GeradorDeOndas()

def run(stream):
  print("Running")
  Ondas.definir_fluxo_bits(stream)
  Ondas.definir_energia(1)
  Ondas.definir_precisao(100)
  Ondas.definir_frequencias(1, 2)
  Ondas.gerar_ondas_digitais()
  Ondas.gerar_ondas_analogicas()
