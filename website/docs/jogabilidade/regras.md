---
id: regras
title: Regras da partida
sidebar_position: 2
---

import Sprite from '@site/src/components/Sprite';

# Regras da partida

## Objetivo

Derrotar o **Boss** antes que as vidas ou o tempo acabem.

## Valores iniciais

| Item | Valor |
|---|---|
| Vidas | 10 (máximo também é 10) |
| Pontuação | 0 |
| Tempo | 5 minutos (300 segundos) |

## Inimigos

<div className="sprite-row">
  <Sprite arquivo="nave.png" legenda="Jogador" />
  <Sprite arquivo="nave_inimiga.png" legenda="Inimigo" />
</div>

- Um novo inimigo surge a cada **50 quadros** (cerca de 0,8 segundo a 60 FPS), em posição horizontal aleatória acima da tela.
- Cada inimigo desce com velocidade aleatória entre **2 e 4** pixels por quadro.
- Eles medem 70 x 70 pixels. A nave do jogador mede 80 x 80.

## Pontos, vidas e dano

| Evento | Resultado |
|---|---|
| Tiro acerta inimigo | Inimigo some e o jogador ganha **+10 pontos** |
| Inimigo morto | 20% de chance de soltar um [power-up](./powerups.md) |
| Inimigo bate na nave | O inimigo some e o jogador perde **1 vida** (sem perda se o escudo estiver ativo) |
| Inimigo passa do fundo da tela | O jogador perde **1 vida** (o escudo não protege neste caso) |
| Bolha do Boss acerta a nave | Perde **1 vida** (sem perda com escudo) |
| Boss encosta na nave | Perde **1 vida** (sem perda com escudo) e a nave é empurrada 30 pixels para a esquerda |
| Vidas chegam a 0 | **Game Over** |

## Chegada do Boss

Quando a pontuação atinge **100 pontos** (10 inimigos destruídos), o Boss é criado. Nesse momento:

- Todos os inimigos que estavam na tela são removidos.
- Novos inimigos **deixam de aparecer**.
- Começa a luta contra o chefe. Veja [Boss](./boss.md).

## Como a partida termina

| Resultado | Condição | Valor gravado no banco |
|---|---|---|
| **VOCE VENCEU!** | A vida do Boss chega a 0 | `vitoria` |
| **GAME OVER** | As vidas chegam a 0 | `game_over` |
| **TEMPO ESGOTADO** | O cronômetro de 5 minutos chega a zero | `tempo_esgotado` |

Ao terminar, o resultado é salvo automaticamente no [ranking](../banco-de-dados.md) e a tela mostra *Pressione R para jogar novamente*.
