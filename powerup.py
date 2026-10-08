import pygame
import random


class PowerUp:

    TIPOS = ("tiro_duplo", "vida", "escudo")

    CORES = {
        "tiro_duplo": (0, 220, 255),
        "vida": (50, 255, 100),
        "escudo": (190, 80, 255)
    }

    SIMBOLOS = {
        "tiro_duplo": "D",
        "vida": "+",
        "escudo": "S"
    }

    def __init__(self, x, y, tipo=None):

        self.x = int(x)
        self.y = int(y)

        self.tipo = tipo or random.choice(self.TIPOS)

        self.tamanho = 30
        self.velocidade = 2

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.tamanho,
            self.tamanho
        )

        self.fonte = pygame.font.Font(None, 25)

    def mover(self):

        self.y += self.velocidade
        self.rect.topleft = (self.x, self.y)

    def desenhar(self, tela):

        cor = self.CORES[self.tipo]

        pygame.draw.circle(
            tela,
            tuple(c // 3 for c in cor),
            self.rect.center,
            19
        )

        pygame.draw.circle(
            tela,
            cor,
            self.rect.center,
            14
        )

        pygame.draw.circle(
            tela,
            (255, 255, 255),
            self.rect.center,
            14,
            2
        )

        simbolo = self.fonte.render(
            self.SIMBOLOS[self.tipo],
            True,
            (10, 10, 30)
        )

        tela.blit(
            simbolo,
            simbolo.get_rect(center=self.rect.center)
        )
