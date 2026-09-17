import pygame


class Bullet:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.largura = 6
        self.altura = 15

        self.velocidade = 8

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.largura,
            self.altura
        )

    def mover(self):

        self.y -= self.velocidade

        self.rect.x = self.x
        self.rect.y = self.y

    def desenhar(self, tela):

        pygame.draw.rect(
            tela,
            (255, 230, 50),
            (
                self.x,
                self.y,
                self.largura,
                self.altura
            )
        )