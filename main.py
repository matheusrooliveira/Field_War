
import pygame
import sys
import random
import traceback

from menu import menu
from player import Player
from enemy import Enemy
from bullet import Bullet
from boss import Boss
from powerup import PowerUp

from sistemas.login import TelaLogin
from sistemas.ranking import (
    inicializar_banco,
    registrar_jogador,
    salvar_recorde
)
from sistemas.timer import Timer


# =========================================
# INICIALIZAÇÃO
# =========================================

pygame.init()

LARGURA = 1000
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("FIELD WAR")

clock = pygame.time.Clock()

PRETO = (5, 5, 20)
BRANCO = (255, 255, 255)
VERMELHO = (255, 50, 50)
VERDE = (50, 255, 100)
CIANO = (0, 220, 255)
ROXO = (190, 80, 255)

fonte = pygame.font.Font(None, 36)
fonte_game_over = pygame.font.Font(None, 70)


# =========================================
# LOGIN
# =========================================

def realizar_login():

    login_tela = TelaLogin()

    fonte_titulo = pygame.font.Font(None, 60)
    fonte_texto = pygame.font.Font(None, 36)

    while True:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            resultado = login_tela.processar_evento(evento)

            if resultado:
                return resultado

        tela.fill(PRETO)

        login_tela.desenhar(
            tela,
            fonte_titulo,
            fonte_texto
        )

        pygame.display.flip()
        clock.tick(60)


# =========================================
# INIMIGOS
# =========================================

def criar_inimigo():

    x = random.randint(20, LARGURA - 60)
    y = random.randint(-100, -40)

    return Enemy(x, y)


# =========================================
# REINICIAR PARTIDA
# =========================================

def reiniciar_jogo():

    jogador = Player(
        LARGURA // 2 - 25,
        ALTURA - 80,
        LARGURA,
        ALTURA
    )

    return {
        "jogador": jogador,
        "inimigos": [],
        "tiros": [],
        "bolhas": [],
        "powerups": [],
        "boss": None,
        "pontuacao": 0,
        "vidas": 10,
        "boss_ativado": False,
        "game_over": False,
        "vitoria": False,
        "tempo_esgotado": False,
        "tempo_inimigo": 0,
        "recorde_salvo": False
    }


# =========================================
# DESENHAR HUD
# =========================================

def desenhar_hud(estado, timer):

    jogador = estado["jogador"]

    texto_pontos = fonte.render(
        f"Pontuação: {estado['pontuacao']}",
        True,
        BRANCO
    )

    texto_vidas = fonte.render(
        f"Vidas: {estado['vidas']}",
        True,
        BRANCO
    )

    texto_timer = fonte.render(
        f"Tempo: {timer.formatar()}",
        True,
        BRANCO
    )

    # Pontuação no canto superior esquerdo
    tela.blit(texto_pontos, (20, 20))

    # Vidas no canto superior direito
    tela.blit(
        texto_vidas,
        (
            LARGURA - texto_vidas.get_width() - 20,
            20
        )
    )

    # Timer logo abaixo das vidas
    tela.blit(
        texto_timer,
        (
            LARGURA - texto_timer.get_width() - 20,
            60
        )
    )

    # Power-ups ativos
    if jogador.tiro_duplo_ativo:

        texto = fonte.render(
            "TIRO DUPLO",
            True,
            CIANO
        )

        tela.blit(texto, (20, 60))

    if jogador.escudo_ativo:

        texto = fonte.render(
            "ESCUDO ATIVO",
            True,
            ROXO
        )

        tela.blit(texto, (20, 100))


# =========================================
# DESENHAR RESULTADO
# =========================================

def desenhar_resultado(estado):

    if estado["game_over"]:

        titulo = "GAME OVER"
        cor = VERMELHO

    elif estado["vitoria"]:

        titulo = "VOCE VENCEU!"
        cor = VERDE

    elif estado["tempo_esgotado"]:

        titulo = "TEMPO ESGOTADO"
        cor = VERMELHO

    else:
        return

    texto = fonte_game_over.render(
        titulo,
        True,
        cor
    )

    reiniciar = fonte.render(
        "Pressione R para jogar novamente",
        True,
        BRANCO
    )

    tela.blit(
        texto,
        (
            LARGURA // 2 - texto.get_width() // 2,
            240
        )
    )

    tela.blit(
        reiniciar,
        (
            LARGURA // 2 - reiniciar.get_width() // 2,
            330
        )
    )


# =========================================
# SALVAR RESULTADO
# =========================================

def salvar_resultado(estado, login, timer):

    if estado["recorde_salvo"]:
        return

    if estado["vitoria"]:
        resultado = "vitoria"

    elif estado["game_over"]:
        resultado = "game_over"

    else:
        resultado = "tempo_esgotado"

    tempo_gasto = 300 - timer.tempo_restante()

    salvar_recorde(
        login,
        estado["pontuacao"],
        resultado,
        tempo_gasto
    )

    estado["recorde_salvo"] = True


# =========================================
# EXECUTAR PARTIDA
# =========================================

def executar_jogo(login):

    estado = reiniciar_jogo()

    timer = Timer(300)
    timer.iniciar()

    estrelas = []

    for _ in range(80):

        estrelas.append([
            random.randint(0, LARGURA),
            random.randint(0, ALTURA),
            random.randint(1, 3)
        ])

    rodando = True

    while rodando:

        clock.tick(60)

        # =====================================
        # EVENTOS
        # =====================================

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                return False

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_SPACE:

                    if not (
                        estado["game_over"]
                        or estado["vitoria"]
                        or estado["tempo_esgotado"]
                    ):

                        jogador = estado["jogador"]

                        if jogador.tiro_duplo_ativo:

                            posicoes = [
                                jogador.x + jogador.largura // 2 - 12,
                                jogador.x + jogador.largura // 2 + 6
                            ]

                        else:

                            posicoes = [
                                jogador.x + jogador.largura // 2 - 3
                            ]

                        for x_tiro in posicoes:

                            estado["tiros"].append(
                                Bullet(x_tiro, jogador.y)
                            )

                if evento.key == pygame.K_r:

                    if (
                        estado["game_over"]
                        or estado["vitoria"]
                        or estado["tempo_esgotado"]
                    ):

                        estado = reiniciar_jogo()
                        timer.reiniciar()

                if evento.key == pygame.K_ESCAPE:
                    return False

        # =====================================
        # TIMER
        # =====================================

        if not (
            estado["game_over"]
            or estado["vitoria"]
            or estado["tempo_esgotado"]
        ):

            if timer.acabou():
                estado["tempo_esgotado"] = True

        # =====================================
        # GAMEPLAY
        # =====================================

        if not (
            estado["game_over"]
            or estado["vitoria"]
            or estado["tempo_esgotado"]
        ):

            jogador = estado["jogador"]

            jogador.mover()

            # -----------------------------
            # POWER-UPS
            # -----------------------------

            for item in estado["powerups"][:]:

                item.mover()

                if item.rect.top > ALTURA:

                    estado["powerups"].remove(item)
                    continue

                if jogador.rect.colliderect(item.rect):

                    if item.tipo == "vida":

                        estado["vidas"] = min(
                            estado["vidas"] + 1,
                            10
                        )

                    elif item.tipo == "tiro_duplo":

                        jogador.ativar_powerup("tiro_duplo")

                    elif item.tipo == "escudo":

                        jogador.ativar_powerup("escudo")

                    estado["powerups"].remove(item)

            # -----------------------------
            # TIROS
            # -----------------------------

            for tiro in estado["tiros"][:]:

                tiro.mover()

                if tiro.y < 0:
                    estado["tiros"].remove(tiro)

            # -----------------------------
            # BOSS AOS 100 PONTOS
            # -----------------------------

            if (
                estado["pontuacao"] >= 100
                and not estado["boss_ativado"]
            ):

                print("Preparando boss...")

                estado["boss"] = Boss(
                    LARGURA,
                    ALTURA,
                    jogador
                )

                estado["boss_ativado"] = True
                estado["inimigos"].clear()

                print("BOSS DESBLOQUEADO!")

            # -----------------------------
            # CRIAR INIMIGOS
            # -----------------------------

            if not estado["boss_ativado"]:

                estado["tempo_inimigo"] += 1

                if estado["tempo_inimigo"] >= 50:

                    estado["inimigos"].append(
                        criar_inimigo()
                    )

                    estado["tempo_inimigo"] = 0

            # -----------------------------
            # MOVIMENTAR INIMIGOS
            # -----------------------------

            for inimigo in estado["inimigos"][:]:

                inimigo.mover()

                if inimigo.y > ALTURA:

                    estado["inimigos"].remove(inimigo)
                    estado["vidas"] -= 1

                    if estado["vidas"] <= 0:

                        estado["vidas"] = 0
                        estado["game_over"] = True

            # -----------------------------
            # TIRO X INIMIGO
            # -----------------------------

            for tiro in estado["tiros"][:]:

                for inimigo in estado["inimigos"][:]:

                    if tiro.rect.colliderect(inimigo.rect):

                        if tiro in estado["tiros"]:
                            estado["tiros"].remove(tiro)

                        if inimigo in estado["inimigos"]:
                            estado["inimigos"].remove(inimigo)

                        estado["pontuacao"] += 10

                        if random.random() < 0.20:

                            estado["powerups"].append(
                                PowerUp(inimigo.x, inimigo.y)
                            )

                        break

            # -----------------------------
            # JOGADOR X INIMIGO
            # -----------------------------

            for inimigo in estado["inimigos"][:]:

                if jogador.rect.colliderect(inimigo.rect):

                    estado["inimigos"].remove(inimigo)

                    if not jogador.escudo_ativo:
                        estado["vidas"] -= 1

                    if estado["vidas"] <= 0:

                        estado["vidas"] = 0
                        estado["game_over"] = True

            # -----------------------------
            # BOSS
            # -----------------------------

            boss = estado["boss"]

            if estado["boss_ativado"] and boss is not None:

                boss.mover(estado["bolhas"])

                # Tiros atingindo escudos
                for tiro in estado["tiros"][:]:

                    if boss.tiro_bateu_no_escudo(tiro):

                        estado["tiros"].remove(tiro)

                # Tiros atingindo o boss
                for tiro in estado["tiros"][:]:

                    if tiro.rect.colliderect(boss.rect):

                        estado["tiros"].remove(tiro)

                        boss.vida -= 1

                        if boss.vida <= 0:

                            boss.vida = 0
                            estado["boss"] = None
                            estado["vitoria"] = True
                            break

                # Bolhas
                if estado["boss"] is not None:

                    for bolha in estado["bolhas"][:]:

                        bolha.mover()

                        if bolha.fora_da_tela(LARGURA, ALTURA):

                            estado["bolhas"].remove(bolha)
                            continue

                        if bolha.rect.colliderect(jogador.rect):

                            estado["bolhas"].remove(bolha)

                            if not jogador.escudo_ativo:
                                estado["vidas"] -= 1

                            if estado["vidas"] <= 0:

                                estado["vidas"] = 0
                                estado["game_over"] = True

                # Boss x jogador
                if estado["boss"] is not None:

                    if jogador.rect.colliderect(estado["boss"].rect):

                        if not jogador.escudo_ativo:
                            estado["vidas"] -= 1

                        jogador.x -= 30

                        if jogador.x < 0:
                            jogador.x = 0

                        jogador.rect.x = int(jogador.x)

                        if estado["vidas"] <= 0:

                            estado["vidas"] = 0
                            estado["game_over"] = True

        # =====================================
        # SALVAR RESULTADO
        # =====================================

        if (
            estado["game_over"]
            or estado["vitoria"]
            or estado["tempo_esgotado"]
        ):

            salvar_resultado(
                estado,
                login,
                timer
            )

        # =====================================
        # DESENHAR
        # =====================================

        tela.fill(PRETO)

        # Estrelas
        for estrela in estrelas:

            pygame.draw.circle(
                tela,
                BRANCO,
                (estrela[0], estrela[1]),
                estrela[2]
            )

            estrela[1] += 1

            if estrela[1] > ALTURA:

                estrela[1] = 0
                estrela[0] = random.randint(0, LARGURA)

        # Jogador
        estado["jogador"].desenhar(tela)

        # Tiros
        for tiro in estado["tiros"]:
            tiro.desenhar(tela)

        # Inimigos
        for inimigo in estado["inimigos"]:
            inimigo.desenhar(tela)

        # Power-ups
        for item in estado["powerups"]:
            item.desenhar(tela)

        # Bolhas
        for bolha in estado["bolhas"]:
            bolha.desenhar(tela)

        # Boss
        if estado["boss"] is not None:
            estado["boss"].desenhar(tela)

        # HUD
        desenhar_hud(estado, timer)

        # Resultado
        desenhar_resultado(estado)

        pygame.display.flip()

    return True


# =========================================
# PROGRAMA PRINCIPAL
# =========================================

def main():

    inicializar_banco()

    login = realizar_login()

    registrar_jogador(login)

    while True:

        jogar = menu(tela, clock)

        if not jogar:
            break

        continuar = executar_jogo(login)

        if not continuar:
            break

    pygame.quit()
    sys.exit()


# =========================================
# EXECUÇÃO COM TRATAMENTO DE ERRO
# =========================================

if __name__ == "__main__":

    try:

        main()

    except Exception:

        traceback.print_exc()

        input(
            "\nOcorreu um erro. Pressione ENTER para fechar..."
        )

        pygame.quit()
        sys.exit(1)
