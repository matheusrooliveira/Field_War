---
id: como-executar
title: Como executar
sidebar_position: 2
---

# Como executar o jogo

## Requisitos

- Python 3.12 ou superior
- Git
- Pygame Community Edition (instalado pelo `requirements.txt`)

## Passo a passo

### 1. Clonar o repositório

```bash
git clone https://github.com/matheusrooliveira/Field_War.git
```

### 2. Entrar na pasta do projeto

```bash
cd Field_War
```

### 3. Criar um ambiente virtual

```bash
python -m venv venv
```

### 4. Ativar o ambiente

**Windows:**

```bash
venv\Scripts\activate
```

**Linux ou macOS:**

```bash
source venv/bin/activate
```

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6. Iniciar o jogo

```bash
python main.py
```

:::warning Execute a partir da raiz do projeto
As imagens são carregadas com caminhos relativos (por exemplo, `assents/nave.png`). Se o jogo for iniciado de outra pasta, o Pygame não encontrará os arquivos e o jogo fecha com erro. Sempre rode `python main.py` dentro da pasta `Field_War`.
:::

## O que acontece ao iniciar

1. O banco de dados SQLite é criado (se ainda não existir) em `database/records.db`.
2. A tela de **login** pede um nome de jogador.
3. O **menu** é exibido: Jogar, Ranking ou Sair.
4. Ao escolher **Jogar**, a partida começa com cronômetro de 5 minutos.

Se ocorrer algum erro inesperado, o programa imprime o traceback e aguarda você pressionar ENTER antes de fechar, o que facilita ler a mensagem.

## Rodando esta documentação

O site que você está lendo fica na pasta `website/` do repositório.

```bash
cd website
npm install
npm start
```

O site abre em `http://localhost:3000/Field_War/`. Para gerar a versão de produção:

```bash
npm run build
npm run serve
```

Requer Node.js 20 ou superior.
