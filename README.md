# Handy Input

## Índice
1. [Introdução](#introdução)
2. [Instalação](#instalação)
    - [Pré-Requisitos](#pré-requisitos)
    - [Download do Projeto](#download-do-projeto)
    - [Configuração do Ambiente Virtual](#configuração-do-ambiente-virtual)
    - [Execução do Projeto](#execução-do-projeto)
5. [Uso](#uso)

## Introdução

Este projeto utiliza a biblioteca **MediaPipe Hands** para criar um sistema de controle de mouse por gestos, transformando gestos de mão capturados pela webcam em comandos de movimento e clique. Usando **OpenCV** para capturar as imagens da câmera, o programa detecta e interpreta gestos específicos que permitem ao usuário executar ações básicas e avançadas com o cursor, como:

* Mover o cursor
* Clicar com o botão esquerdo e direito
* Arrastar
* Scrollar

A ideia é oferecer uma experiência interativa e intuitiva de controle, onde a mão funciona como um "trackpad virtual", permitindo a navegação sem a necessidade de periféricos físicos.

## Instalação

Para garantir que todas as dependências do projeto sejam instaladas corretamente e que não haja conflitos com outras bibliotecas do sistema, recomenda-se o uso de um ambiente virtual. Siga os passos abaixo para configurar o ambiente:

**Esse guia de instalação foi feito para Linux Ubuntu. Os comandos podem ter alguma variação em outros sistemas operacionais.**

### Pré-requisitos

* Certifique-se de que você possui o **Python 3.12** ou superior instalado em sua máquina. Você pode verificar a versão do Python instalada executando o seguinte comando no terminal:

```
python --version
```

ou

```
python3 --version
```

* Certifique-se também que você possui o **python3-venv** instalado.

Para instalá-lo **(Linux Ubuntu)**:

```
sudo apt install python3-venv
```

### Download do Projeto:

Clone o repositório usando o comando:

```
git clone https://github.com/CantarinoG/handy-input.git
```

### Configuração do Ambiente Virtual:

* Para criar um ambiente virtual, execute o seguinte comando estando no diretório do projeto:

```
python -m venv env
```

ou

```
python3 -m venv env
```

* Para ativar o ambiente virtual, execute o comando:

```
source env/bin/activate
```

* Para instalar as dependências do projeto, execute o comando:

```
pip install -r requirements.txt
```

### Execução do Projeto:

* Para executar o projeto, execute o comando:

```
python src/main.py
```