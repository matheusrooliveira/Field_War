import pygame
import random

class Enemy:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.largura = 70
        self.altura = 70

        self.velocidade = random.randint(2, 4)

        # Carrega a imagem do inimigo
        self.imagem = pygame.image.load(
            "assents/nave_inimiga.png"
        ).convert_alpha()

        # Redimensiona o inimigo
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

        self.y += self.velocidade

        self.rect.x = self.x
        self.rect.y = self.y

    def desenhar(self, tela):

        tela.blit(
            self.imagem,
            (self.x, self.y)
        )