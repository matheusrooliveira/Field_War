
import pygame


class Bullet:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # Dimensões do projétil
        self.largura = 18
        self.altura = 38

        self.velocidade = 8

        self.rect = pygame.Rect(
            self.x - self.largura // 2,
            self.y,
            self.largura,
            self.altura
        )

    def mover(self):
        self.y -= self.velocidade

        self.rect.centerx = self.x
        self.rect.y = self.y

    def desenhar(self, tela):
        # Superfície transparente para criar o brilho
        brilho = pygame.Surface(
            (self.largura * 4, self.altura * 2),
            pygame.SRCALPHA
        )

        cx = brilho.get_width() // 2
        cy = brilho.get_height() // 2

        # Camadas externas de energia azul
        pygame.draw.ellipse(
            brilho,
            (0, 50, 255, 35),
            (cx - 15, cy - 27, 30, 54)
        )

        pygame.draw.ellipse(
            brilho,
            (0, 100, 255, 75),
            (cx - 10, cy - 23, 20, 46)
        )

        # Corpo pontudo do projétil
        pygame.draw.polygon(
            brilho,
            (0, 70, 255, 220),
            [
                (cx, cy - 19),
                (cx + 7, cy - 5),
                (cx + 5, cy + 13),
                (cx, cy + 20),
                (cx - 5, cy + 13),
                (cx - 7, cy - 5)
            ]
        )

        # Núcleo ciano
        pygame.draw.polygon(
            brilho,
            (0, 230, 255, 255),
            [
                (cx, cy - 16),
                (cx + 4, cy - 4),
                (cx + 3, cy + 13),
                (cx, cy + 17),
                (cx - 3, cy + 13),
                (cx - 4, cy - 4)
            ]
        )

        # Centro branco e brilhante
        pygame.draw.polygon(
            brilho,
            (255, 255, 255, 255),
            [
                (cx, cy - 10),
                (cx + 2, cy - 2),
                (cx + 2, cy + 10),
                (cx, cy + 14),
                (cx - 2, cy + 10),
                (cx - 2, cy - 2)
            ]
        )

        # Pequenas partículas laterais
        for dx, dy, tamanho in [
            (-9, -5, 3),
            (9, -5, 3),
            (-8, 4, 2),
            (8, 4, 2),
            (-6, 12, 2),
            (6, 12, 2)
        ]:
            pygame.draw.rect(
                brilho,
                (0, 180, 255, 230),
                (
                    cx + dx - tamanho // 2,
                    cy + dy - tamanho // 2,
                    tamanho,
                    tamanho
                )
            )

        # Desenha o efeito centralizado no projétil
        tela.blit(
            brilho,
            (
                self.x - cx,
                self.y - cy
            )
        )