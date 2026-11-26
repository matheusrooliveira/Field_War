---
id: ciclo-do-jogo
title: Ciclo do jogo
sidebar_position: 3
---

# Ciclo do jogo

## Fluxo geral do programa

```mermaid
flowchart TD
    A([python main.py]) --> B[inicializar_banco]
    B --> C[Tela de login]
    C --> D[registrar_jogador]
    D --> E{Menu}
    E -- Ranking --> R[Tela de ranking] --> E
    E -- Sair --> Z([Fim])
    E -- Jogar --> F[executar_jogo]
    F --> G{Partida terminou?}
    G -- Esc ou fechar janela --> Z
    G -- R pressionado --> F
```

## Um quadro da partida (60 por segundo)

A cada iteração de `executar_jogo()`, nesta ordem:

```mermaid
flowchart TD
    S([Início do quadro]) --> EV[Tratar eventos<br/>espaço, R, Esc, fechar]
    EV --> TM{Tempo acabou?}
    TM -- sim --> TE[tempo_esgotado = True]
    TM -- não --> ATIVO{Partida ativa?}
    TE --> ATIVO
    ATIVO -- sim --> PL[Mover jogador]
    PL --> PW[Power-ups: mover e coletar]
    PW --> TI[Mover tiros]
    TI --> BS{Pontos >= 100<br/>e boss ainda não criado?}
    BS -- sim --> BC[Criar Boss<br/>limpar inimigos]
    BS -- não --> SP
    BC --> SP[Gerar inimigo se não há boss<br/>a cada 50 quadros]
    SP --> EN[Mover inimigos<br/>perder vida se passarem]
    EN --> CT[Colisões: tiro x inimigo<br/>jogador x inimigo]
    CT --> BB[Boss: mover, escudos,<br/>tiros, bolhas, contato]
    BB --> SV
    ATIVO -- não --> SV[Salvar recorde se terminou]
    SV --> DR[Desenhar fundo, entidades,<br/>HUD e resultado]
    DR --> FL[display.flip]
    FL --> S
```

## Estados da partida

```mermaid
stateDiagram-v2
    [*] --> Jogando
    Jogando --> BossAtivo: pontuação chega a 100
    Jogando --> GameOver: vidas chegam a 0
    Jogando --> TempoEsgotado: 5 minutos
    BossAtivo --> Vitoria: vida do boss chega a 0
    BossAtivo --> GameOver: vidas chegam a 0
    BossAtivo --> TempoEsgotado: 5 minutos
    Vitoria --> Jogando: tecla R
    GameOver --> Jogando: tecla R
    TempoEsgotado --> Jogando: tecla R
```

O estado é representado por flags booleanas no dicionário `estado` (`boss_ativado`, `game_over`, `vitoria`, `tempo_esgotado`). Enquanto qualquer uma das três flags finais está ativa, o gameplay é congelado, mas a tela continua sendo desenhada.

## Detecção de colisão

Todas as entidades possuem um `pygame.Rect` (`rect`) atualizado a cada movimento. As colisões usam `Rect.colliderect()`, com exceção dos **escudos do Boss**, que usam distância euclidiana (`math.hypot`) entre o tiro e o centro de cada escudo.

## Persistência do resultado

Quando a partida termina, `salvar_resultado()` grava o recorde uma única vez (controle pela flag `recorde_salvo`). O tempo gasto é calculado como `300 - tempo_restante`.
