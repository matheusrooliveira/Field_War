import pygame
import math


class Boss:

    def __init__(self, largura_tela, altura_tela, jogador):

        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.jogador = jogador

        # =========================================
        # TAMANHO
        # =========================================

        self.largura = 220
        self.altura = 160

        self.imagem = pygame.image.load(
            "assents/boss.png"
        ).convert_alpha()

        self.imagem = pygame.transform.scale(
            self.imagem,
            (self.largura, self.altura)
        )

        # =========================================
        # POSIÇÃO
        # =========================================

        self.x = (
            largura_tela // 2
            - self.largura // 2
        )

        self.y = 50

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.largura,
            self.altura
        )

        # =========================================
        # VIDA
        # =========================================

        self.vida_maxima = 60
        self.vida = self.vida_maxima

        # =========================================
        # MOVIMENTO
        # =========================================

        self.direcao = 1

        # =========================================
        # ATAQUE
        # =========================================

        self.timer_ataque = 0

        # =========================================
        # FASE
        # =========================================

        self.fase = 1

        # =========================================
        # ESCUDOS
        # =========================================

        self.angulo_escudo = 0
        self.raio_orbita = 150
        self.raio_escudo = 55
        self.pos_escudos = []

        # =========================================
        # ATRAÇÃO
        # =========================================

        self.raio_atracao = 450

    # =============================================
    # MOVIMENTO DO BOSS
    # =============================================

    def mover(self, bolhas):

        # =========================================
        # FASES
        # =========================================

        if self.vida > 40:

            self.fase = 1
            velocidade = 3
            intervalo_ataque = 90

        elif self.vida > 20:

            self.fase = 2
            velocidade = 5
            intervalo_ataque = 60

        else:

            self.fase = 3
            velocidade = 7
            intervalo_ataque = 35

        # =========================================
        # MOVIMENTO HORIZONTAL
        # =========================================

        self.x += velocidade * self.direcao

        if self.x <= 0:

            self.x = 0
            self.direcao = 1

        if self.x + self.largura >= self.largura_tela:

            self.x = (
                self.largura_tela
                - self.largura
            )

            self.direcao = -1

        # =========================================
        # MOVIMENTO VERTICAL
        # =========================================

        self.y = (
            50
            + math.sin(
                pygame.time.get_ticks() / 300
            ) * 15
        )

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # =========================================
        # ATAQUE
        # =========================================

        self.timer_ataque += 1

        if self.timer_ataque >= intervalo_ataque:

            self.timer_ataque = 0

            bolhas.append(
                self.criar_bolha()
            )

        # =========================================
        # ESCUDOS
        # =========================================

        self.atualizar_escudos()

        # =========================================
        # ATRAÇÃO
        # =========================================

        self.atracao_magnetica()

    # =============================================
    # ATRAÇÃO MAGNÉTICA
    # =============================================

    def atracao_magnetica(self):

        # Centro do jogador

        jogador_x = self.jogador.rect.centerx
        jogador_y = self.jogador.rect.centery

        # Centro do Boss

        boss_x = self.rect.centerx
        boss_y = self.rect.centery

        # Distância entre eles

        dx = boss_x - jogador_x
        dy = boss_y - jogador_y

        distancia = math.hypot(
            dx,
            dy
        )

        # =========================================
        # VERIFICAR ALCANCE
        # =========================================

        if distancia > self.raio_atracao:

            return

        if distancia <= 1:

            return

        # =========================================
        # FORÇA DA ATRAÇÃO
        # =========================================

        if self.fase == 1:

            forca = 2.0

        elif self.fase == 2:

            forca = 3.5

        else:

            forca = 5.0

        # =========================================
        # DIREÇÃO
        # =========================================

        dx /= distancia
        dy /= distancia

        # =========================================
        # PUXAR PLAYER
        # =========================================

        self.jogador.x += dx * forca
        self.jogador.y += dy * forca

        # =========================================
        # LIMITES DA TELA
        # =========================================

        if self.jogador.x < 0:

            self.jogador.x = 0

        if self.jogador.x + self.jogador.largura > self.largura_tela:

            self.jogador.x = (
                self.largura_tela
                - self.jogador.largura
            )

        if self.jogador.y < 0:

            self.jogador.y = 0

        if self.jogador.y + self.jogador.altura > self.altura_tela:

            self.jogador.y = (
                self.altura_tela
                - self.jogador.altura
            )

        # =========================================
        # ATUALIZAR COLISÃO
        # =========================================

        self.jogador.rect.x = int(
            self.jogador.x
        )

        self.jogador.rect.y = int(
            self.jogador.y
        )

    # =============================================
    # CRIAR BOLHA
    # =============================================

    def criar_bolha(self):

        from bolha import Bolha

        return Bolha(
            self.rect.centerx,
            self.rect.bottom,
            self.jogador.rect.centerx,
            self.jogador.rect.centery
        )

    # =============================================
    # ESCUDOS
    # =============================================

    def atualizar_escudos(self):

        self.pos_escudos = []

        if self.fase < 2:

            return

        self.angulo_escudo += 0.05

        for deslocamento in [0, math.pi]:

            x = (
                self.rect.centerx
                + math.cos(
                    self.angulo_escudo
                    + deslocamento
                ) * self.raio_orbita
            )

            y = (
                self.rect.centery
                + math.sin(
                    self.angulo_escudo
                    + deslocamento
                ) * self.raio_orbita
            )

            self.pos_escudos.append(
                (x, y)
            )

    # =============================================
    # TIRO NO ESCUDO
    # =============================================

    def tiro_bateu_no_escudo(self, tiro):

        if self.fase < 2:

            return False

        for x, y in self.pos_escudos:

            distancia = math.hypot(
                tiro.rect.centerx - x,
                tiro.rect.centery - y
            )

            if distancia <= self.raio_escudo:

                return True

        return False

    # =============================================
    # DESENHAR
    # =============================================

    def desenhar(self, tela):

        tela.blit(
            self.imagem,
            (self.x, self.y)
        )

        self.desenhar_escudos(
            tela
        )

        self.desenhar_vida(
            tela
        )

    # =============================================
    # DESENHAR ESCUDOS
    # =============================================

    def desenhar_escudos(self, tela):

        if self.fase < 2:

            return

        superficie = pygame.Surface(
            (
                self.raio_escudo * 2,
                self.raio_escudo * 2
            ),
            pygame.SRCALPHA
        )

        if self.fase == 2:

            alfa = 70

        else:

            alfa = 130

        pygame.draw.circle(
            superficie,
            (255, 0, 0, alfa),
            (
                self.raio_escudo,
                self.raio_escudo
            ),
            self.raio_escudo
        )

        for x, y in self.pos_escudos:

            tela.blit(
                superficie,
                (
                    x - self.raio_escudo,
                    y - self.raio_escudo
                )
            )

    # =============================================
    # BARRA DE VIDA
    # =============================================

    def desenhar_vida(self, tela):

        largura_barra = 300
        altura_barra = 15

        porcentagem = (
            self.vida
            / self.vida_maxima
        )

        largura_atual = int(
            largura_barra
            * porcentagem
        )

        x = (
            self.largura_tela // 2
            - largura_barra // 2
        )

        y = 20

        pygame.draw.rect(
            tela,
            (80, 0, 0),
            (
                x,
                y,
                largura_barra,
                altura_barra
            )
        )

        if self.fase == 1:

            cor = (40, 200, 70)

        elif self.fase == 2:

            cor = (255, 220, 0)

        else:

            cor = (255, 80, 20)

        if largura_atual > 0:

            pygame.draw.rect(
                tela,
                cor,
                (
                    x,
                    y,
                    largura_atual,
                    altura_barra
                )
            )

        fonte = pygame.font.Font(
            None,
            24
        )

        texto = fonte.render(
            f"BOSS  {self.vida}/{self.vida_maxima}",
            True,
            (255, 255, 255)
        )

        texto_rect = texto.get_rect(
            center=(
                self.largura_tela // 2,
                y + altura_barra // 2
            )
        )

        tela.blit(
            texto,
            texto_rect
        )