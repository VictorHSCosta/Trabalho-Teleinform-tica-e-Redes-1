from imagens import GeradorDeOndas

gerador_test = GeradorDeOndas()

gerador_test.definir_fluxo_bits([1, 0, 1, 1, 0, 0, 1, 1])
gerador_test.definir_energia(1)
gerador_test.definir_precisao(100)
gerador_test.definir_frequencias(1, 2)
gerador_test.gerar_ondas_digitais()
gerador_test.gerar_ondas_analogicas()


