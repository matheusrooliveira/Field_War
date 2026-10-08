import pygame
import random


class PowerUp:

    TIPOS = ("tiro_duplo", "vida", "escudo")

    CORES = {
        "tiro_duplo": (0, 190, 255),
        "vida": (50, 220, 90),
        "escudo": (170, 80, 255)
    }

    def __init__(self, x, y, tipo=None):

        self.x = int(x)
        self.y = int(y)

        self.tipo = tipo or random.choice(self.TIPOS)

        self.tamanho = 36
        self.velocidade = 2

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.tamanho,
            self.tamanho
        )

    # =====================================
    # MOVIMENTAR POWER-UP
    # =====================================

    def mover(self):

        self.y += self.velocidade
        self.rect.topleft = (self.x, self.y)

    # =====================================
    # DESENHAR POWER-UP
    # =====================================

    def desenhar(self, tela):

        centro_x, centro_y = self.rect.center
        cor = self.CORES[self.tipo]

        # Fundo circular escuro
        pygame.draw.circle(
            tela,
            (18, 25, 38),
            (centro_x, centro_y),
            19
        )

        # Anel exterior
        pygame.draw.circle(
            tela,
            cor,
            (centro_x, centro_y),
            18,
            2
        )

        # DETALHES MILITARES
        if self.tipo == "tiro_duplo":

            # Dois projéteis apontados para cima
            for deslocamento in (-7, 7):

                px = centro_x + deslocamento

                # Corpo do projétil
                pygame.draw.rect(
                    tela,
                    cor,
                    (px - 3, centro_y - 7, 6, 15)
                )

                # Ponta do projétil
                pygame.draw.polygon(
                    tela,
                    (210, 245, 255),
                    [
                        (px, centro_y - 13),
                        (px - 4, centro_y - 6),
                        (px + 4, centro_y - 6)
                    ]
                )

                # Aletas
                pygame.draw.polygon(
                    tela,
                    cor,
                    [
                        (px - 3, centro_y + 3),
                        (px - 7, centro_y + 8),
                        (px - 3, centro_y + 7)
                    ]
                )

                pygame.draw.polygon(
                    tela,
                    cor,
                    [
                        (px + 3, centro_y + 3),
                        (px + 7, centro_y + 8),
                        (px + 3, centro_y + 7)
                    ]
                )

        elif self.tipo == "vida":

            # Cruz médica verde
            pygame.draw.rect(
                tela,
                cor,
                (centro_x - 5, centro_y - 12, 10, 24)
            )

            pygame.draw.rect(
                tela,
                cor,
                (centro_x - 12, centro_y - 5, 24, 10)
            )

            # Pequeno detalhe central
            pygame.draw.rect(
                tela,
                (220, 255, 225),
                (centro_x - 2, centro_y - 9, 4, 18)
            )

        elif self.tipo == "escudo":

            # Escudo com formato militar
            pontos = [
                (centro_x, centro_y - 13),
                (centro_x + 11, centro_y - 8),
                (centro_x + 9, centro_y + 5),
                (centro_x, centro_y + 13),
                (centro_x - 9, centro_y + 5),
                (centro_x - 11, centro_y - 8)
            ]

            pygame.draw.polygon(
                tela,
                cor,
                pontos
            )

            # Centro escuro do escudo
            pontos_internos = [
                (centro_x, centro_y - 8),
                (centro_x + 7, centro_y - 5),
                (centro_x + 6, centro_y + 4),
                (centro_x, centro_y + 9),
                (centro_x - 6, centro_y + 4),
                (centro_x - 7, centro_y - 5)
            ]

            pygame.draw.polygon(
                tela,
                (35, 22, 55),
                pontos_internos
            )

            # Estrela central simples
            pygame.draw.polygon(
                tela,
                (235, 220, 255),
                [
                    (centro_x, centro_y - 6),
                    (centro_x + 2, centro_y - 1),
                    (centro_x + 7, centro_y - 1),
                    (centro_x + 3, centro_y + 2),
                    (centro_x + 5, centro_y + 7),
                    (centro_x, centro_y + 4),
                    (centro_x - 5, centro_y + 7),
                    (centro_x - 3, centro_y + 2),
                    (centro_x - 7, centro_y - 1),
                    (centro_x - 2, centro_y - 1)
                ]
            )
