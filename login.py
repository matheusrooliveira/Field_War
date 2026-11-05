import pygame


class TelaLogin:

    def __init__(self):
        self.login = ""
        self.max_caracteres = 16

    def processar_evento(self, evento):

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_RETURN:

                if self.login.strip():
                    return self.login.strip()

            elif evento.key == pygame.K_BACKSPACE:

                self.login = self.login[:-1]

            else:
                caractere = evento.unicode

                if (
                    caractere.isalnum() or caractere in "_-"
                ) and len(self.login) < self.max_caracteres:

                    self.login += caractere

        return None

    def desenhar(self, tela, fonte_titulo, fonte_texto):

        tela.fill((5, 8, 20))

        titulo = fonte_titulo.render(
            "FIELD WAR",
            True,
            (0, 200, 255)
        )

        subtitulo = fonte_texto.render(
            "DIGITE SEU LOGIN PARA CONTINUAR",
            True,
            (255, 255, 255)
        )

        campo = fonte_texto.render(
            self.login + "|",
            True,
            (0, 255, 180)
        )

        instrucao = fonte_texto.render(
            "PRESSIONE ENTER PARA CONTINUAR",
            True,
            (150, 150, 150)
        )

        tela.blit(
            titulo,
            titulo.get_rect(center=(tela.get_width() // 2, 180))
        )

        tela.blit(
            subtitulo,
            subtitulo.get_rect(center=(tela.get_width() // 2, 270))
        )

        pygame.draw.rect(
            tela,
            (0, 200, 255),
            (tela.get_width() // 2 - 180, 310, 360, 50),
            2
        )

        tela.blit(
            campo,
            campo.get_rect(center=(tela.get_width() // 2, 335))
        )

        tela.blit(
            instrucao,
            instrucao.get_rect(center=(tela.get_width() // 2, 410))
        )