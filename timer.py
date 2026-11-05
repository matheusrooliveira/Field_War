import pygame


class Timer:
    def __init__(self, duracao=300):
        self.duracao = duracao
        self.inicio = None
        self.ativo = False

    def iniciar(self):
        self.inicio = pygame.time.get_ticks()
        self.ativo = True

    def parar(self):
        self.ativo = False

    def reiniciar(self):
        self.iniciar()

    def tempo_restante(self):
        if not self.ativo or self.inicio is None:
            return self.duracao

        decorrido = (pygame.time.get_ticks() - self.inicio) // 1000

        return max(0, self.duracao - decorrido)

    def acabou(self):
        return self.ativo and self.tempo_restante() <= 0

    def formatar(self):
        segundos = self.tempo_restante()

        minutos = segundos // 60
        segundos = segundos % 60

        return f"{minutos:02d}:{segundos:02d}"

    def desenhar(self, tela, fonte, cor=(255, 255, 255)):
        texto = fonte.render(
            self.formatar(),
            True,
            cor
        )

        tela.blit(texto, (tela.get_width() - 120, 20))