---
id: audio
title: Áudio
sidebar_position: 7
---

import AudioRow from '@site/src/components/AudioRow';

# Áudio

O jogo tem um **gerenciador de áudio** (`audio.py`) e **17 arquivos `.wav`** em `assents/sons/`: 3 músicas e 14 efeitos sonoros. Todos os sons foram **sintetizados por código** (sem samples de terceiros) pelo script `tools/gerar_audio.py`, usando `numpy`.

:::tip Áudio integrado
O áudio está ligado ao jogo: a música muda conforme a tela (menu, partida e Boss) e os efeitos tocam nos eventos descritos em [Quando cada som toca](#quando-cada-som-toca). Se o computador não tiver dispositivo de áudio, o jogo roda normalmente, só sem som.
:::

## Trilhas

| Nome no código | Arquivo | Uso previsto |
|---|---|---|
| `menu` | `musica_menu.wav` | Menu principal |
| `jogo` | `musica_jogo.wav` | Partida |
| `boss` | `musica_boss.wav` | Luta contra o Boss |

## Efeitos sonoros

| Nome | Arquivo | Volume |
|---|---|---|
| `tiro` | `tiro.wav` | 0,35 |
| `explosao` | `explosao.wav` | 0,60 |
| `dano` | `dano.wav` | 0,70 |
| `powerup` | `powerup.wav` | 0,60 |
| `vida` | `vida.wav` | 0,60 |
| `escudo` | `escudo.wav` | 0,60 |
| `escudo_hit` | `escudo_hit.wav` | 0,50 |
| `boss_entra` | `boss_entra.wav` | 0,80 |
| `boss_hit` | `boss_hit.wav` | 0,50 |
| `boss_tiro` | `boss_tiro.wav` | 0,40 |
| `boss_derrotado` | `boss_derrotado.wav` | 0,80 |
| `vitoria` | `vitoria.wav` | 0,70 |
| `game_over` | `game_over.wav` | 0,70 |
| `clique` | `clique.wav` | 0,50 |

### Ouça alguns exemplos

<AudioRow nome="Tiro" arquivo="tiro.wav" />
<AudioRow nome="Explosão" arquivo="explosao.wav" />
<AudioRow nome="Power-up" arquivo="powerup.wav" />
<AudioRow nome="Entrada do Boss" arquivo="boss_entra.wav" />
<AudioRow nome="Vitória" arquivo="vitoria.wav" />
<AudioRow nome="Game Over" arquivo="game_over.wav" />

## API do gerenciador

O módulo expõe uma instância pronta, `audio`:

```python
from audio import audio

audio.iniciar()            # depois de pygame.init()
audio.musica("menu")       # troca a trilha (não reinicia se já toca)
audio.tocar("tiro")        # efeito sonoro
audio.processar_evento(e)  # tecla M liga/desliga o som
```

Comportamentos de projeto:

- **Tolerante a falhas:** se não houver dispositivo de áudio ou faltar um arquivo, o jogo continua sem som.
- **Anti-metralhadora:** o mesmo efeito não toca duas vezes em menos de 60 ms.
- **Mudo:** a tecla <kbd>M</kbd> alterna o som; ao reativar, a trilha atual volta a tocar.
- **Música em loop**, com *fade-in* de 600 ms e volume 0,45.

## Quando cada som toca

| Momento | Som |
|---|---|
| Menu e tela de login | música `menu` |
| Início da partida (e ao reiniciar com <kbd>R</kbd>) | música `jogo` |
| Boss entra | música `boss` e efeito `boss_entra` |
| Disparo (<kbd>Espaço</kbd>) | `tiro` |
| Inimigo destruído | `explosao` |
| Jogador leva dano (inimigo, bolha ou Boss) | `dano`, ou `escudo_hit` se o escudo estiver ativo |
| Inimigo passa do fundo da tela | `dano` |
| Coletar power-up | `powerup` (tiro duplo), `escudo` ou `vida` |
| Tiro absorvido pelo escudo do Boss | `escudo_hit` |
| Tiro acerta o Boss | `boss_hit` |
| Boss lança uma bolha | `boss_tiro` |
| Boss derrotado | `boss_derrotado` e, em seguida, `vitoria` |
| Game Over ou tempo esgotado | `game_over` |
| Clique em botão do menu ou do ranking | `clique` |

Ao terminar a partida a música é interrompida para dar destaque ao som de vitória ou de derrota.

## Tecla M

Durante o menu e a partida, <kbd>M</kbd> liga e desliga todo o som. O estado aparece no canto inferior esquerdo da partida (`M: SOM LIGADO` ou `M: SOM DESLIGADO`). Na tela de login a tecla M não é interceptada, porque o jogador pode digitar a letra no nome.

## Regenerar os sons

```bash
pip install numpy
python tools/gerar_audio.py
```
