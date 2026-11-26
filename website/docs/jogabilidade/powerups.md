---
id: powerups
title: Power-ups
sidebar_position: 3
---

# Power-ups

Cada inimigo destruído tem **20% de chance** de soltar um power-up. O tipo é sorteado entre os três disponíveis. O item cai a 2 pixels por quadro e desaparece se sair pela parte de baixo da tela. Para coletar, basta encostar a nave nele.

| Power-up | Cor | Efeito | Duração |
|---|---|---|---|
| **Tiro duplo** | Ciano | Cada disparo lança dois projéteis lado a lado | 8 segundos |
| **Vida** | Verde | Recupera 1 vida (até o máximo de 10) | Instantâneo |
| **Escudo** | Roxo | Anula o dano de colisões com inimigos, bolhas e Boss | 5 segundos |

## Detalhes

- Os efeitos de **tiro duplo** e **escudo** são temporários. A classe `Player` guarda o instante em que cada um termina (`tiro_duplo_ate` e `escudo_ate`, em milissegundos) e consulta as propriedades `tiro_duplo_ativo` e `escudo_ativo`.
- Pegar o mesmo power-up de novo enquanto ele está ativo **reinicia** a contagem.
- O escudo é desenhado como uma elipse azul ao redor da nave, e o HUD mostra **ESCUDO ATIVO** ou **TIRO DUPLO** enquanto durarem.
- O escudo **não** impede a perda de vida quando um inimigo atravessa a parte de baixo da tela.
