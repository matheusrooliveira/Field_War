import pygame
import sys
import random

from menu import menu
from player import Player
from enemy import Enemy
from bullet import Bullet


# =========================================
# INICIALIZAÇÃO
# =========================================

pygame.init()


# =========================================
# CONFIGURAÇÕES
# =========================================

LARGURA = 1000
ALTURA = 600

tela = pygame.display.set_mode(
    (LARGURA, ALTURA)
)

pygame.display.set_caption("FIELD WAR")

clock = pygame.time.Clock()


# =========================================
# CORES
# =========================================

PRETO = (5, 5, 20)
BRANCO = (255, 255, 255)
VERMELHO = (255, 50, 50)


# =========================================
# FONTES
# =========================================

fonte = pygame.font.Font(
    None,
    36
)

fonte_game_over = pygame.font.Font(
    None,
    70
)


# =========================================
# ESTRELAS DO JOGO
# =========================================

estrelas = []

for i in range(80):

    x = random.randint(
        0,
        LARGURA
    )

    y = random.randint(
        0,
        ALTURA
    )

    tamanho = random.randint(
        1,
        3
    )

    estrelas.append([
        x,
        y,
        tamanho
    ])


# =========================================
# CRIAR INIMIGO
# =========================================

def criar_inimigo():

    x = random.randint(
        20,
        LARGURA - 60
    )

    y = random.randint(
        -100,
        -40
    )

    return Enemy(
        x,
        y
    )


# =========================================
# REINICIAR JOGO
# =========================================

def reiniciar_jogo():

    jogador = Player(
        LARGURA // 2 - 25,
        ALTURA - 80,
        LARGURA,
        ALTURA
    )

    inimigos = []

    tiros = []

    pontuacao = 0

    vidas = 3

    return (
        jogador,
        inimigos,
        tiros,
        pontuacao,
        vidas
    )


# =========================================
# ABRIR MENU
# =========================================

jogar = menu(
    tela,
    clock
)


# =========================================
# SE CLICOU EM JOGAR
# =========================================

if jogar:

    jogador, inimigos, tiros, pontuacao, vidas = reiniciar_jogo()

    tempo_inimigo = 0

    game_over = False

    rodando = True

    # =====================================
    # LOOP DO JOGO
    # =====================================

    while rodando:

        clock.tick(60)

        # =================================
        # EVENTOS
        # =================================

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                rodando = False

            # -----------------------------
            # TECLAS
            # -----------------------------

            if evento.type == pygame.KEYDOWN:

                # Atirar
                if evento.key == pygame.K_SPACE:

                    if not game_over:

                        novo_tiro = Bullet(
                            jogador.x +
                            jogador.largura // 2 - 3,
                            jogador.y
                        )

                        tiros.append(
                            novo_tiro
                        )

                # Reiniciar
                if evento.key == pygame.K_r:

                    if game_over:

                        (
                            jogador,
                            inimigos,
                            tiros,
                            pontuacao,
                            vidas
                        ) = reiniciar_jogo()

                        game_over = False

        # =================================
        # GAMEPLAY
        # =================================

        if not game_over:

            # -----------------------------
            # JOGADOR
            # -----------------------------

            jogador.mover()

            # -----------------------------
            # TIROS
            # -----------------------------

            for tiro in tiros[:]:

                tiro.mover()

                if tiro.y < 0:

                    tiros.remove(
                        tiro
                    )

            # -----------------------------
            # CRIAR INIMIGOS
            # -----------------------------

            tempo_inimigo += 1

            if tempo_inimigo >= 50:

                inimigos.append(
                    criar_inimigo()
                )

                tempo_inimigo = 0

            # -----------------------------
            # MOVIMENTAR INIMIGOS
            # -----------------------------

            for inimigo in inimigos[:]:

                inimigo.mover()

                # Inimigo passou pela tela
                if inimigo.y > ALTURA:

                    inimigos.remove(
                        inimigo
                    )

                    vidas -= 1

                    if vidas <= 0:

                        game_over = True

            # -----------------------------
            # TIRO X INIMIGO
            # -----------------------------

            for tiro in tiros[:]:

                for inimigo in inimigos[:]:

                    if tiro.rect.colliderect(
                        inimigo.rect
                    ):

                        if tiro in tiros:

                            tiros.remove(
                                tiro
                            )

                        if inimigo in inimigos:

                            inimigos.remove(
                                inimigo
                            )

                        pontuacao += 10

                        break

            # -----------------------------
            # JOGADOR X INIMIGO
            # -----------------------------

            for inimigo in inimigos[:]:

                if jogador.rect.colliderect(
                    inimigo.rect
                ):

                    inimigos.remove(
                        inimigo
                    )

                    vidas -= 1

                    if vidas <= 0:

                        game_over = True

        # =================================
        # DESENHAR FUNDO
        # =================================

        tela.fill(
            PRETO
        )

        # =================================
        # ESTRELAS
        # =================================

        for estrela in estrelas:

            pygame.draw.circle(
                tela,
                BRANCO,
                (
                    estrela[0],
                    estrela[1]
                ),
                estrela[2]
            )

            estrela[1] += 1

            if estrela[1] > ALTURA:

                estrela[1] = 0

                estrela[0] = random.randint(
                    0,
                    LARGURA
                )

        # =================================
        # DESENHAR JOGADOR
        # =================================

        jogador.desenhar(
            tela
        )

        # =================================
        # DESENHAR TIROS
        # =================================

        for tiro in tiros:

            tiro.desenhar(
                tela
            )

        # =================================
        # DESENHAR INIMIGOS
        # =================================

        for inimigo in inimigos:

            inimigo.desenhar(
                tela
            )

        # =================================
        # INTERFACE
        # =================================

        texto_pontos = fonte.render(
            f"Pontuação: {pontuacao}",
            True,
            BRANCO
        )

        texto_vidas = fonte.render(
            f"Vidas: {vidas}",
            True,
            BRANCO
        )

        tela.blit(
            texto_pontos,
            (20, 20)
        )

        tela.blit(
            texto_vidas,
            (850, 20)
        )

        # =================================
        # GAME OVER
        # =================================

        if game_over:

            texto = fonte_game_over.render(
                "GAME OVER",
                True,
                VERMELHO
            )

            texto_reiniciar = fonte.render(
                "Pressione R para reiniciar",
                True,
                BRANCO
            )

            tela.blit(
                texto,
                (
                    LARGURA // 2 -
                    texto.get_width() // 2,
                    240
                )
            )

            tela.blit(
                texto_reiniciar,
                (
                    LARGURA // 2 -
                    texto_reiniciar.get_width() // 2,
                    330
                )
            )

        # =================================
        # ATUALIZAR TELA
        # =================================

        pygame.display.flip()


# =========================================
# ENCERRAR
# =========================================

pygame.quit()

sys.exit()