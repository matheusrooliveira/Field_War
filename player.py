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

        # Carrega a imagem da nave
        self.imagem = pygame.image.load(
            "assents/nave.png"
        ).convert_alpha()

        # Redimensiona a nave
        self.imagem = pygame.transform.scale(
            self.imagem,
            (self.largura, self.altura)
        )

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.largura,
            self.altura
        )

    def mover(self):

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= self.velocidade

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += self.velocidade

        if self.x < 0:
            self.x = 0

        if self.x + self.largura > self.largura_tela:
            self.x = self.largura_tela - self.largura

        self.rect.x = self.x
        self.rect.y = self.y

    def desenhar(self, tela):

        tela.blit(
            self.imagem,
            (self.x, self.y)
        )