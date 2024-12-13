```markdown
# Trabalho de Teleinformática e Redes 1

Este projeto foi desenvolvido como parte do trabalho da disciplina **Teleinformática e Redes 1**. Ele consiste em uma aplicação de transmissor que utiliza Node.js e Python para execução. Siga as instruções abaixo para configurar e executar o projeto no Linux.

## Pré-requisitos

Antes de começar, certifique-se de que você possui os seguintes itens instalados em sua máquina:

- **Node.js** (caso vá utilizar a execução via `npm run dev`)
- **Python 3** (caso vá utilizar os scripts `dev.sh` e `start.sh`)
- **Virtualenv** (para gerenciar o ambiente virtual do Python)

## Como usar no Linux

### 1. Clonar o repositório

Primeiro, faça o clone do projeto para a sua máquina local:
```bash
git clone <URL_DO_REPOSITORIO>
```
Substitua `<URL_DO_REPOSITORIO>` pelo link do repositório GitHub.

### 2. Acessar o diretório do projeto

Abra o terminal e navegue até a pasta principal do projeto:
```bash
cd <nome_da_pasta_do_projeto>
```

### 3. Configurar permissões para os scripts

Conceda permissão de execução para os scripts `dev.sh` e `start.sh`:
```bash
chmod +x dev.sh
chmod +x start.sh
```

Esses comandos são necessários para que os scripts possam ser executados no terminal.

### 4. Executar o projeto com Node.js

Se você possui o Node.js instalado, execute o seguinte comando no terminal para iniciar o transmissor:
```bash
npm run dev
```
> ⚠️ **Importante:** Certifique-se de que o Node.js está instalado em sua distro antes de usar este comando.

### 5. Executar o projeto com Python

Caso você **não tenha o Node.js instalado**, você pode rodar o projeto utilizando os scripts disponíveis. Para isso:

1. Ative o ambiente virtual Python:
   ```bash
   source venv/bin/activate
   ```

2. Execute o script de configuração inicial:
   ```bash
   python3 config.py
   ```

3. Por fim, execute o script principal:
   ```bash
   python3 main.py
   ```

## Scripts disponíveis

- **`dev.sh`**: Contém os comandos necessários para ativar o ambiente virtual e configurar o projeto:
  ```bash
  #!/bin/bash
  source venv/bin/activate
  python3 config.py
  ```

- **`start.sh`**: Executa o script principal:
  ```bash
  #!/bin/bash
  python3 main.py
  ```

Certifique-se de que ambos os scripts possuem permissão de execução para que funcionem corretamente.

## Sobre o projeto

Este trabalho foi criado para fins educacionais na disciplina de Teleinformática e Redes 1, sendo um transmissor básico com suporte a execução em **Node.js** e **Python**. Ele explora conceitos fundamentais de redes e integração entre linguagens de programação.

## Contribuições

Se desejar contribuir para este projeto, sinta-se à vontade para abrir issues ou pull requests no repositório.


```
