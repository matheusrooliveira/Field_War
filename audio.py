"""
Sistema de áudio do Field War.

Uso:

    from audio import audio

    audio.iniciar()            # depois de pygame.init()
    audio.musica("menu")       # troca a trilha (não reinicia se já toca)
    audio.tocar("tiro")        # efeito sonoro
    audio.processar_evento(e)  # tecla M liga/desliga o som

Se o dispositivo de áudio não estiver disponível ou algum arquivo faltar,
o jogo continua normalmente, apenas sem som.
"""

import os

import pygame

PASTA_SONS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assents",
    "sons",
)

MUSICAS = {
    "menu": "musica_menu.wav",
    "jogo": "musica_jogo.wav",
    "boss": "musica_boss.wav",
}

EFEITOS = {
    "tiro": ("tiro.wav", 0.35),
    "explosao": ("explosao.wav", 0.6),
    "dano": ("dano.wav", 0.7),
    "powerup": ("powerup.wav", 0.6),
    "vida": ("vida.wav", 0.6),
    "escudo": ("escudo.wav", 0.6),
    "escudo_hit": ("escudo_hit.wav", 0.5),
    "boss_entra": ("boss_entra.wav", 0.8),
    "boss_hit": ("boss_hit.wav", 0.5),
    "boss_tiro": ("boss_tiro.wav", 0.4),
    "boss_derrotado": ("boss_derrotado.wav", 0.8),
    "vitoria": ("vitoria.wav", 0.7),
    "game_over": ("game_over.wav", 0.7),
    "clique": ("clique.wav", 0.5),
}

# Intervalo mínimo (ms) entre duas execuções do mesmo efeito, para evitar
# "metralhadora" de sons quando algo acontece vários frames seguidos.
INTERVALO_MIN_MS = 60

VOLUME_MUSICA = 0.45


class GerenciadorAudio:

    def __init__(self):
        self.ativo = False
        self.mudo = False
        self.musica_atual = None
        self._tocando = None
        self._sons = {}
        self._ultimo = {}

    # -------------------------------------
    # INICIALIZAÇÃO
    # -------------------------------------

    def iniciar(self):

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            pygame.mixer.set_num_channels(16)
            pygame.mixer.music.set_volume(VOLUME_MUSICA)

        except pygame.error as erro:
            print(f"[audio] sem dispositivo de áudio: {erro}")
            self.ativo = False
            return False

        for nome, (arquivo, volume) in EFEITOS.items():

            caminho = os.path.join(PASTA_SONS, arquivo)

            try:
                som = pygame.mixer.Sound(caminho)
                som.set_volume(volume)
                self._sons[nome] = som

            except (pygame.error, FileNotFoundError) as erro:
                print(f"[audio] não carregou '{arquivo}': {erro}")

        self.ativo = True
        return True

    # -------------------------------------
    # EFEITOS
    # -------------------------------------

    def tocar(self, nome):

        if not self.ativo or self.mudo:
            return

        som = self._sons.get(nome)

        if som is None:
            return

        agora = pygame.time.get_ticks()

        if agora - self._ultimo.get(nome, -10_000) < INTERVALO_MIN_MS:
            return

        self._ultimo[nome] = agora
        som.play()

    # -------------------------------------
    # MÚSICA
    # -------------------------------------

    def musica(self, nome, fade_ms=600):
        """Toca a trilha em loop. Não faz nada se ela já estiver tocando."""

        self.musica_atual = nome

        if not self.ativo:
            return

        arquivo = MUSICAS.get(nome)

        if arquivo is None:
            return

        if self.mudo:
            # lembra qual trilha deveria tocar; começa quando desmutar
            return

        try:
            if pygame.mixer.music.get_busy() and self._tocando == nome:
                return

            pygame.mixer.music.load(os.path.join(PASTA_SONS, arquivo))
            pygame.mixer.music.set_volume(VOLUME_MUSICA)
            pygame.mixer.music.play(-1, fade_ms=fade_ms)
            self._tocando = nome

        except (pygame.error, FileNotFoundError) as erro:
            print(f"[audio] não tocou '{arquivo}': {erro}")

    def parar_musica(self):
        # stop() em vez de fadeout(): o fadeout do pygame bloqueia o jogo
        # até terminar.

        self.musica_atual = None
        self._tocando = None

        if not self.ativo:
            return

        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass

    # -------------------------------------
    # MUDO (tecla M)
    # -------------------------------------

    def alternar_mudo(self):

        self.mudo = not self.mudo

        if not self.ativo:
            return

        if self.mudo:
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            self._tocando = None

        elif self.musica_atual:
            self.musica(self.musica_atual, fade_ms=200)

    def processar_evento(self, evento):
        """Chame em todo loop de eventos. Retorna True se tratou a tecla."""

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_m:
            self.alternar_mudo()
            return True

        return False

    def texto_status(self):
        return "M: SOM DESLIGADO" if self.mudo else "M: SOM LIGADO"


audio = GerenciadorAudio()
