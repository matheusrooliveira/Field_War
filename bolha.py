import pygame
import math


class Bolha:
    def __init__(self, x, y, alvo_x, alvo_y):
        self.raio = 12

        self.x = x
        self.y = y

        dx = alvo_x - x
        dy = alvo_y - y

        distancia = math.hypot(dx, dy)

        if distancia != 0:
            dx /= distancia
            dy /= distancia

        self.velocidade = 3.5

        self.vel_x = dx * self.velocidade
        self.vel_y = dy * self.velocidade

        self.rect = pygame.Rect(
            int(self.x - self.raio),
            int(self.y - self.raio),
            self.raio * 2,
            self.raio * 2
        )

    def mover(self):
        self.x += self.vel_x
        self.y += self.vel_y

        self.rect.x = int(self.x - self.raio)
        self.rect.y = int(self.y - self.raio)

    def desenhar(self, tela):
        superficie = pygame.Surface(
            (self.raio * 2, self.raio * 2),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            superficie,
            (135, 206, 235, 180),
            (self.raio, self.raio),
            self.raio
        )

        pygame.draw.circle(
            superficie,
            (255, 255, 255, 210),
            (self.raio - 4, self.raio - 4),
            4
        )

        tela.blit(
            superficie,
            self.rect
        )

    def fora_da_tela(self, largura, altura):
        return (
            self.rect.right < 0 or
            self.rect.left > largura or
            self.rect.bottom < 0 or
            self.rect.top > altura
        )