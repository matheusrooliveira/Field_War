---
id: modulos
title: Módulos e classes
sidebar_position: 2
---

# Módulos e classes

## `main.py`

Ponto de entrada. Define a janela (1000 x 600), o `clock` de 60 FPS e as funções:

| Função | Papel |
|---|---|
| `realizar_login()` | Laço da tela de login; devolve o nome digitado |
| `criar_inimigo()` | Cria um `Enemy` em posição aleatória acima da tela |
| `reiniciar_jogo()` | Devolve um dicionário `estado` com tudo zerado (jogador, listas, vidas, flags) |
| `desenhar_hud()` | Pontuação, vidas, tempo e power-ups ativos |
| `desenhar_resultado()` | Texto de vitória, Game Over ou tempo esgotado |
| `salvar_resultado()` | Grava o recorde uma única vez por partida |
| `executar_jogo(login)` | Laço de uma partida |
| `main()` | Inicializa o banco, faz o login e alterna entre menu e partida |

O estado de uma partida é um **dicionário** (`estado`) com chaves como `jogador`, `inimigos`, `tiros`, `bolhas`, `powerups`, `boss`, `pontuacao`, `vidas`, `boss_ativado`, `game_over`, `vitoria` e `tempo_esgotado`.

## `player.py` : `Player`

| Membro | Descrição |
|---|---|
| `x`, `y`, `largura`, `altura` | Posição e tamanho (80 x 80) |
| `velocidade` | 12 pixels por quadro |
| `rect` | Área de colisão |
| `tiro_duplo_ate`, `escudo_ate` | Instante (ms) em que cada power-up termina |
| `ativar_powerup(tipo)` | Define a duração: 8 s (`tiro_duplo`) ou 5 s (`escudo`) |
| `tiro_duplo_ativo`, `escudo_ativo` | Propriedades booleanas |
| `mover()` | Lê o teclado e limita a nave à tela |
| `desenhar(tela)` | Desenha a nave e o anel do escudo |

## `enemy.py` : `Enemy`

Nave de 70 x 70 que desce com velocidade aleatória de 2 a 4. Métodos `mover()` e `desenhar(tela)`.

## `bullet.py` : `Bullet`

Projétil de 18 x 38 pixels, velocidade 8, que sobe a tela. O desenho é feito por código, com camadas de elipses e polígonos (azul, ciano e branco) para criar efeito de brilho.

## `boss.py` : `Boss`

Maior classe do projeto. Controla vida (60), fase, movimento, ataque, atração magnética, escudos e barra de vida.

| Método | Papel |
|---|---|
| `mover(bolhas)` | Escolhe a fase pela vida, move o boss, dispara bolhas e chama escudos e atração |
| `atracao_magnetica()` | Puxa o jogador quando ele está a menos de 450 px |
| `criar_bolha()` | Cria uma `Bolha` mirando o jogador |
| `atualizar_escudos()` | Calcula a posição dos dois escudos orbitais (fase 2 em diante) |
| `tiro_bateu_no_escudo(tiro)` | Verifica se o tiro foi absorvido por um escudo |
| `desenhar`, `desenhar_escudos`, `desenhar_vida` | Renderização |

## `bolha.py` : `Bolha`

Projétil do Boss: raio 12, velocidade 3,5, direção calculada no momento da criação (vetor normalizado até o alvo). Possui `fora_da_tela(largura, altura)` para descarte.

## `powerup.py` : `PowerUp`

Item de 36 x 36 que cai a 2 px por quadro. Tem a constante `TIPOS = ("tiro_duplo", "vida", "escudo")` e um dicionário `CORES`. Cada tipo é desenhado com um ícone próprio dentro de um círculo.

## `menu.py`

| Função | Papel |
|---|---|
| `menu(tela, clock)` | Menu animado (foguetes e explosões no fundo) com os botões JOGAR, RANKING e SAIR. Devolve `True` para jogar e `False` para sair |
| `tela_ranking(tela, clock)` | Mostra o Top 10 com posição, jogador, pontos e tempo |

## `sistemas/login.py` : `TelaLogin`

Guarda o texto digitado (máximo de 16 caracteres; aceita letras, números, `_` e `-`). `processar_evento(evento)` devolve o nome quando o jogador pressiona ENTER com texto não vazio.

## `sistemas/timer.py` : `Timer`

Cronômetro baseado em `pygame.time.get_ticks()`. Duração padrão de 300 s. Métodos: `iniciar`, `parar`, `reiniciar`, `tempo_restante`, `acabou`, `formatar` (formato `MM:SS`) e `desenhar`.

## `sistemas/ranking.py`

Funções de acesso ao SQLite. Detalhes em [Banco de dados](../banco-de-dados.md).

## `audio.py`

Gerenciador de áudio (`GerenciadorAudio`). Veja a página [Áudio](../audio.md) com a lista de sons e o momento em que cada um toca.
