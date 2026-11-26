---
id: melhorias-futuras
title: Melhorias futuras
sidebar_position: 9
---

# Melhorias futuras

## Previstas no README

- ~~Trilha sonora e efeitos sonoros~~ (já implementados, ver [Áudio](./audio.md))
- Novos tipos de inimigos e mecânicas de combate
- Efeitos visuais e animações mais elaborados
- Progressão de dificuldade e jogabilidade expandida
- Melhorias de interface e experiência do usuário

## Sugestões a partir da análise do código

| Tema | Sugestão |
|---|---|
| Herança | Criar as classes-base `EntidadeJogo`, `EntidadeComImagem` e `Projetil` previstas nos [diagramas](./arquitetura/diagramas.md) e remover a repetição de `x`, `y` e `rect` |
| Carregamento de imagens | `Player` e `Enemy` carregam o PNG do disco a cada instância (`Enemy` a cada inimigo criado). Carregar uma vez e reutilizar melhora o desempenho |
| Caminhos | Usar `pathlib` a partir de `__file__`, como o `ranking.py` já faz, para o jogo abrir de qualquer pasta |
| Estado da partida | Trocar o dicionário `estado` por uma classe `Partida`, e dividir `executar_jogo()` (mais de 400 linhas) em funções menores |
| Constantes | Concentrar valores fixos (vidas, 300 s, 100 pontos para o Boss, durações dos power-ups) em um arquivo de configuração |
| Dificuldade | Aumentar a velocidade e a frequência dos inimigos ao longo do tempo antes do Boss |
| Pasta `assents` | O nome está escrito diferente de *assets*; renomear exige atualizar todos os caminhos no código |
| Documentação | A publicação no GitHub Pages é automática pelo workflow `.github/workflows/deploy-docs.yml` (ver abaixo) |

## Publicação automática da documentação

O workflow `deploy-docs.yml` gera e publica o site a cada push na `main` que mude a pasta `website/`. Para ele funcionar, no GitHub abra **Settings, Pages** e, em **Source**, escolha **GitHub Actions**. Isso exige permissão de administrador no repositório.
