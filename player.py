import pygame


class Player:

    def __init__(self, x, y, largura_tela, altura_tela):

        self.x = x
        self.y = y

        self.largura = 80
        self.altura = 80

        self.velocidade = 12

        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

        # Power-ups temporários (tempo em milissegundos)
        self.tiro_duplo_ate = 0
        self.escudo_ate = 0

        # CARREGAR IMAGEM DA NAVE
        self.imagem = pygame.image.load(
            "assents/nave.png"
        ).convert_alpha()

        # REDIMENSIONAR NAVE
        self.imagem = pygame.transform.scale(
            self.imagem,
            (self.largura, self.altura)
        )

        # ÁREA DE COLISÃO
        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.largura,
            self.altura
        )

    # ATIVAR POWER-UPS
    def ativar_powerup(self, tipo):

        agora = pygame.time.get_ticks()

        if tipo == "tiro_duplo":
            self.tiro_duplo_ate = agora + 8000

        elif tipo == "escudo":
            self.escudo_ate = agora + 5000

    # VERIFICAR POWER-UPS ATIVOS
    @property
    def tiro_duplo_ativo(self):
        return pygame.time.get_ticks() < self.tiro_duplo_ate

    @property
    def escudo_ativo(self):
        return pygame.time.get_ticks() < self.escudo_ate

    # MOVIMENTO
    def mover(self):

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= self.velocidade

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += self.velocidade

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.y -= self.velocidade

        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.y += self.velocidade

        # LIMITES HORIZONTAIS
        if self.x < 0:
            self.x = 0

        if self.x + self.largura > self.largura_tela:
            self.x = self.largura_tela - self.largura

        # LIMITES VERTICAIS
        if self.y < 0:
            self.y = 0

        if self.y + self.altura > self.altura_tela:
            self.y = self.altura_tela - self.altura

        # ATUALIZAR RECT
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    # DESENHAR
    def desenhar(self, tela):

        tela.blit(
            self.imagem,
            (self.x, self.y)
        )

        # DESENHAR ESCUDO ATIVO
        if self.escudo_ativo:

            pygame.draw.ellipse(
                tela,
                (100, 180, 255),
                (
                    self.rect.x - 8,
                    self.rect.y - 8,
                    self.rect.width + 16,
                    self.rect.height + 16
                ),
                3
            )
