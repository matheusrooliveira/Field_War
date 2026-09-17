import pygame
import random


# -----------------------------------------
# CORES
# -----------------------------------------

PRETO = (5, 5, 12)
VERMELHO = (220, 40, 30)
LARANJA = (255, 120, 20)
AMARELO = (255, 220, 80)
BRANCO = (255, 255, 255)


# -----------------------------------------
# FUNÇÃO DO MENU
# -----------------------------------------

def menu(tela, clock):

    LARGURA = 1000
    ALTURA = 600

    # Fontes
    fonte_titulo = pygame.font.Font(None, 100)
    fonte_botao = pygame.font.Font(None, 50)
    fonte_pequena = pygame.font.Font(None, 28)

    # -----------------------------------------
    # ESTRELAS
    # -----------------------------------------

    estrelas = []

    for _ in range(100):

        x = random.randint(0, LARGURA)
        y = random.randint(0, ALTURA)
        tamanho = random.randint(1, 3)

        estrelas.append([x, y, tamanho])

    # -----------------------------------------
    # FOGUETES
    # -----------------------------------------

    foguetes = []

    def criar_foguete():

        x = random.randint(-200, LARGURA)
        y = random.randint(80, 350)

        velocidade = random.uniform(4, 8)

        foguetes.append({
            "x": x,
            "y": y,
            "velocidade": velocidade
        })

    # -----------------------------------------
    # EXPLOSÕES
    # -----------------------------------------

    explosoes = []

    def criar_explosao(x, y):

        explosoes.append({
            "x": x,
            "y": y,
            "raio": 5,
            "vida": 30
        })

    # -----------------------------------------
    # DESENHAR FOGUETE
    # -----------------------------------------

    def desenhar_foguete(foguete):

        x = foguete["x"]
        y = foguete["y"]

        # Corpo
        pygame.draw.ellipse(
            tela,
            (180, 180, 190),
            (x, y, 35, 12)
        )

        # Ponta
        pygame.draw.polygon(
            tela,
            BRANCO,
            [
                (x + 35, y),
                (x + 50, y + 6),
                (x + 35, y + 12)
            ]
        )

        # Fogo
        pygame.draw.polygon(
            tela,
            LARANJA,
            [
                (x, y + 2),
                (x - 20, y + 6),
                (x, y + 10)
            ]
        )

        pygame.draw.polygon(
            tela,
            AMARELO,
            [
                (x, y + 4),
                (x - 12, y + 6),
                (x, y + 8)
            ]
        )

    # -----------------------------------------
    # DESENHAR EXPLOSÃO
    # -----------------------------------------

    def desenhar_explosao(explosao):

        x = explosao["x"]
        y = explosao["y"]
        raio = explosao["raio"]

        pygame.draw.circle(
            tela,
            VERMELHO,
            (int(x), int(y)),
            raio
        )

        pygame.draw.circle(
            tela,
            LARANJA,
            (int(x), int(y)),
            max(1, raio - 5)
        )

        pygame.draw.circle(
            tela,
            AMARELO,
            (int(x), int(y)),
            max(1, raio - 10)
        )

    # -----------------------------------------
    # BOTÃO
    # -----------------------------------------

    def desenhar_botao(texto, x, y, largura, altura, mouse):

        rect = pygame.Rect(
            x,
            y,
            largura,
            altura
        )

        if rect.collidepoint(mouse):

            cor = (180, 35, 30)
            borda = (255, 180, 60)

        else:

            cor = (80, 20, 25)
            borda = (160, 50, 40)

        pygame.draw.rect(
            tela,
            cor,
            rect,
            border_radius=10
        )

        pygame.draw.rect(
            tela,
            borda,
            rect,
            3,
            border_radius=10
        )

        texto_render = fonte_botao.render(
            texto,
            True,
            BRANCO
        )

        texto_rect = texto_render.get_rect(
            center=rect.center
        )

        tela.blit(
            texto_render,
            texto_rect
        )

        return rect

    # -----------------------------------------
    # LOOP DO MENU
    # -----------------------------------------

    rodando = True

    tempo_foguete = 0

    while rodando:

        clock.tick(60)

        mouse = pygame.mouse.get_pos()

        # -----------------------------------------
        # EVENTOS
        # -----------------------------------------

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                return False

            if evento.type == pygame.MOUSEBUTTONDOWN:

                # JOGAR
                if botao_jogar.collidepoint(evento.pos):

                    return True

                # SAIR
                if botao_sair.collidepoint(evento.pos):

                    return False

        # -----------------------------------------
        # FUNDO
        # -----------------------------------------

        tela.fill(PRETO)

        # Estrelas
        for estrela in estrelas:

            pygame.draw.circle(
                tela,
                (120, 120, 140),
                (estrela[0], estrela[1]),
                estrela[2]
            )

        # -----------------------------------------
        # FOGUETES
        # -----------------------------------------

        tempo_foguete += 1

        if tempo_foguete > 45:

            criar_foguete()

            tempo_foguete = 0

        for foguete in foguetes[:]:

            foguete["x"] += foguete["velocidade"]

            desenhar_foguete(foguete)

            if foguete["x"] > LARGURA:

                criar_explosao(
                    LARGURA - 50,
                    foguete["y"]
                )

                foguetes.remove(foguete)

        # -----------------------------------------
        # EXPLOSÕES
        # -----------------------------------------

        for explosao in explosoes[:]:

            desenhar_explosao(explosao)

            explosao["raio"] += 2
            explosao["vida"] -= 1

            if explosao["vida"] <= 0:

                explosoes.remove(explosao)

        # -----------------------------------------
        # CHÃO
        # -----------------------------------------

        pygame.draw.rect(
            tela,
            (25, 30, 25),
            (0, 450, LARGURA, 150)
        )

        # Montanhas
        pygame.draw.polygon(
            tela,
            (18, 20, 20),
            [
                (0, 450),
                (150, 350),
                (300, 450),
                (450, 330),
                (650, 450),
                (800, 360),
                (1000, 450),
                (1000, 600),
                (0, 600)
            ]
        )

        # -----------------------------------------
        # TÍTULO
        # -----------------------------------------

        titulo = fonte_titulo.render(
            "FIELD WAR",
            True,
            VERMELHO
        )

        titulo_sombra = fonte_titulo.render(
            "FIELD WAR",
            True,
            (50, 0, 0)
        )

        titulo_rect = titulo.get_rect(
            center=(LARGURA // 2, 150)
        )

        tela.blit(
            titulo_sombra,
            (
                titulo_rect.x + 6,
                titulo_rect.y + 6
            )
        )

        tela.blit(
            titulo,
            titulo_rect
        )

        # -----------------------------------------
        # SUBTÍTULO
        # -----------------------------------------

        subtitulo = fonte_pequena.render(
            "THE ROCKET WAR",
            True,
            (190, 190, 190)
        )

        subtitulo_rect = subtitulo.get_rect(
            center=(LARGURA // 2, 220)
        )

        tela.blit(
            subtitulo,
            subtitulo_rect
        )

        # -----------------------------------------
        # BOTÕES
        # -----------------------------------------

        botao_jogar = desenhar_botao(
            "JOGAR",
            350,
            300,
            300,
            65,
            mouse
        )

        botao_sair = desenhar_botao(
            "SAIR",
            350,
            390,
            300,
            65,
            mouse
        )

        # -----------------------------------------
        # RODAPÉ
        # -----------------------------------------

        texto = fonte_pequena.render(
            "Prepare-se para a batalha...",
            True,
            (120, 120, 120)
        )

        tela.blit(
            texto,
            (20, ALTURA - 40)
        )

        pygame.display.flip()

    return False