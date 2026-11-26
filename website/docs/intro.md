---
id: intro
title: Visão geral
slug: /intro
sidebar_position: 1
---

# Field War

> **ONE MISSION. ONE BATTLEFIELD. NO SECOND CHANCES.**

**Field War** é um jogo 2D de nave (*space shooter*) desenvolvido em **Python** com **Pygame Community Edition**. Em um universo hostil, o jogador pilota sua nave, sobrevive a ondas de inimigos, coleta power-ups e enfrenta um chefe poderoso, tudo dentro de uma partida de **cinco minutos**.

O projeto foi desenvolvido em equipe, como trabalho acadêmico do curso de Ciência da Computação. Ele aplica conceitos de programação orientada a objetos, lógica de programação, detecção de colisão, gerenciamento de estados e persistência de dados.

## Principais recursos

| Recurso | Descrição |
|---|---|
| Login do jogador | O jogador se identifica antes de jogar (até 16 caracteres) |
| Menu principal | Navegação por mouse: Jogar, Ranking e Sair |
| Combate | Tiro simples ou duplo e destruição de inimigos |
| Inimigos | Naves que descem a tela em velocidades aleatórias |
| Boss | Chefe com 60 de vida, 3 fases, escudos orbitais e atração magnética |
| Power-ups | Tiro duplo, escudo e vida extra |
| Vidas | O jogador começa com 10 vidas |
| Cronômetro | Cada partida dura 5 minutos |
| Pontuação | 10 pontos por inimigo destruído |
| Áudio | 3 músicas e 14 efeitos sonoros, com tecla M para silenciar |
| Ranking | Top 10 melhores recordes salvos em SQLite |
| Fim de jogo | Vitória, Game Over ou Tempo Esgotado |

## Por onde começar

- Quer jogar? Veja [Como executar](./como-executar.md).
- Quer entender as regras? Veja [Controles](./jogabilidade/controles.md) e [Regras](./jogabilidade/regras.md).
- Quer entender o código? Veja [Estrutura do projeto](./arquitetura/estrutura.md) e [Diagramas](./arquitetura/diagramas.md).

## Dados rápidos

| | |
|---|---|
| Categoria | Shooter espacial 2D |
| Linguagem | Python 3.12 ou superior |
| Biblioteca gráfica | Pygame CE (`pygame-ce>=2.5.8`) |
| Banco de dados | SQLite |
| Resolução da janela | 1000 x 600 pixels, 60 FPS |
| Repositório | [github.com/matheusrooliveira/Field_War](https://github.com/matheusrooliveira/Field_War) |
