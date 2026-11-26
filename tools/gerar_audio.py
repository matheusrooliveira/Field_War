"""
Gerador de áudio do Field War.

Sintetiza (do zero, sem samples de terceiros) as músicas e os efeitos
sonoros do jogo e grava tudo como WAV na pasta `assents/sons/`.

Uso (a partir da raiz do projeto):

    pip install numpy
    python tools/gerar_audio.py

Os arquivos já vêm gerados no repositório; rode o script só se quiser
alterar timbres, melodias ou volumes.
"""

import os
import wave

import numpy as np

SR = 22050
PASTA_SAIDA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assents",
    "sons",
)

rng = np.random.default_rng(7)


# =========================================
# PRIMITIVAS
# =========================================

def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def onda(tipo, freq, t, duty=0.5):
    """freq pode ser escalar ou array (para glissandos)."""
    if np.isscalar(freq):
        fase = (freq * t) % 1.0
    else:
        fase = (np.cumsum(freq) / SR) % 1.0

    if tipo == "quadrada":
        return np.where(fase < duty, 1.0, -1.0)
    if tipo == "triangulo":
        return 2 * np.abs(2 * fase - 1) - 1
    if tipo == "serra":
        return 2 * fase - 1
    if tipo == "seno":
        return np.sin(2 * np.pi * fase)
    raise ValueError(tipo)


def ruido(n):
    return rng.uniform(-1, 1, n)


def passa_baixa(x, k):
    """Média móvel simples (k amostras): suaviza o ruído."""
    if k <= 1:
        return x
    kernel = np.ones(k) / k
    return np.convolve(x, kernel, mode="same")


def somar(buf, inicio, sinal, circular=False):
    """Soma `sinal` em `buf` a partir de `inicio` (amostras).
    Com circular=True o que passa do fim volta ao começo (loop perfeito)."""
    n = len(buf)
    if circular:
        idx = (inicio + np.arange(len(sinal))) % n
        np.add.at(buf, idx, sinal)
    else:
        fim = min(n, inicio + len(sinal))
        if fim > inicio:
            buf[inicio:fim] += sinal[: fim - inicio]


def envelope(n, ataque=0.004, decaimento=6.0, release=0.02):
    t = np.arange(n) / SR
    env = np.minimum(1.0, t / max(ataque, 1e-4)) * np.exp(-decaimento * t)
    r = int(release * SR)
    if r > 0 and n > r:
        env[-r:] *= np.linspace(1, 0, r)
    return env


def nota(buf, inicio_s, dur_s, midi, tipo, vol, duty=0.5,
         decaimento=6.0, ataque=0.004, circular=True):
    n = int(dur_s * SR)
    t = np.arange(n) / SR
    s = onda(tipo, hz(midi), t, duty) * envelope(n, ataque, decaimento)
    somar(buf, int(inicio_s * SR), s * vol, circular)


def kick(buf, inicio_s, vol=0.9):
    n = int(0.22 * SR)
    t = np.arange(n) / SR
    f = 45 + 120 * np.exp(-t * 28)
    s = onda("seno", f, t) * np.exp(-t * 14)
    somar(buf, int(inicio_s * SR), s * vol, True)


def caixa(buf, inicio_s, vol=0.5):
    n = int(0.16 * SR)
    t = np.arange(n) / SR
    s = (ruido(n) * 0.8 + onda("seno", 190, t) * 0.4) * np.exp(-t * 22)
    somar(buf, int(inicio_s * SR), s * vol, True)


def chimbal(buf, inicio_s, vol=0.18):
    n = int(0.05 * SR)
    t = np.arange(n) / SR
    r = ruido(n)
    r = r - passa_baixa(r, 4)  # passa-alta tosco
    s = r * np.exp(-t * 90)
    somar(buf, int(inicio_s * SR), s * vol, True)


def eco(buf, atraso_s, realimentacao, mistura):
    """Eco circular: mantém o loop sem emendas."""
    d = int(atraso_s * SR)
    saida = buf.copy()
    atual = buf
    for i in range(1, 5):
        atual = np.roll(atual, d) * realimentacao
        saida += atual * mistura
    return saida


def normalizar(x, pico=0.9):
    m = np.max(np.abs(x))
    return x / m * pico if m > 0 else x


def salvar(nome, x):
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    dados = (np.clip(x, -1, 1) * 32767).astype("<i2")
    caminho = os.path.join(PASTA_SAIDA, nome + ".wav")
    with wave.open(caminho, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(dados.tobytes())
    print(f"{nome:16s} {len(x) / SR:6.2f}s  {os.path.getsize(caminho) // 1024:5d} KB")


# =========================================
# MÚSICAS (8 compassos, loop perfeito)
# =========================================

MENOR = (0, 3, 7)
MAIOR = (0, 4, 7)


def musica_menu():
    bpm = 92
    passo = 60 / bpm / 4          # 1/16
    compasso = passo * 16
    total = compasso * 8
    buf = np.zeros(int(total * SR))

    # (raiz grave, acorde, nota da melodia)
    prog = [
        (45, MENOR, [81, None, None, None, 79, None, 76, None]),
        (41, MAIOR, [77, None, None, None, 76, None, 72, None]),
        (48, MAIOR, [79, None, None, None, 76, None, 72, None]),
        (40, MENOR, [71, None, 74, None, 76, None, None, None]),
    ]

    for c in range(8):
        raiz, tipo, mel = prog[c % 4]
        t0 = c * compasso

        # base (pad) em triângulo
        for iv in tipo:
            nota(buf, t0, compasso * 1.05, raiz + 12 + iv, "triangulo",
                 0.16, decaimento=0.6, ataque=0.15)

        # baixo longo
        nota(buf, t0, compasso * 0.98, raiz - 12 + 12, "triangulo",
             0.35, decaimento=0.9, ataque=0.02)

        # arpejo suave
        padrao = [0, 1, 2, 1, 0, 1, 2, 1]
        for i, p in enumerate(padrao * 2):
            nota(buf, t0 + i * passo * 1, passo * 1.8,
                 raiz + 24 + tipo[p], "quadrada", 0.05, duty=0.125,
                 decaimento=7)

        # melodia (a 2ª metade da música sobe uma oitava em alguns trechos)
        for i, m in enumerate(mel):
            if m is not None:
                oit = 12 if (c >= 4 and i == 0) else 0
                nota(buf, t0 + i * passo * 2, passo * 5, m + oit, "triangulo",
                     0.30, decaimento=2.2, ataque=0.01)

    buf = eco(buf, passo * 3, 0.5, 0.45)
    salvar("musica_menu", normalizar(buf, 0.85))


def musica_jogo():
    bpm = 140
    passo = 60 / bpm / 4
    compasso = passo * 16
    total = compasso * 8
    buf = np.zeros(int(total * SR))

    prog = [
        (45, MENOR),   # Am
        (41, MAIOR),   # F
        (48, MAIOR),   # C
        (43, MAIOR),   # G
    ]

    melodia_a = [
        [76, None, 72, 76, 81, None, 79, 76],
        [77, None, 72, 77, 81, None, 79, 77],
        [76, None, 72, 76, 79, None, 76, 72],
        [74, None, 71, 74, 79, None, 78, 74],
    ]
    melodia_b = [
        [81, 81, 79, 76, 79, None, 76, 72],
        [77, 77, 76, 72, 77, None, 81, 77],
        [79, 79, 76, 72, 76, 79, 84, None],
        [83, None, 79, 74, 71, 74, 79, None],
    ]

    for c in range(8):
        raiz, tipo = prog[c % 4]
        t0 = c * compasso

        # baixo em colcheias
        for i in range(8):
            oit = 12 if i % 4 == 3 else 0
            nota(buf, t0 + i * passo * 2, passo * 1.8, raiz + oit,
                 "triangulo", 0.55, decaimento=3)

        # arpejo rápido
        padrao = [0, 1, 2, 1]
        for i in range(16):
            nota(buf, t0 + i * passo, passo * 0.9,
                 raiz + 24 + tipo[padrao[i % 4]], "quadrada", 0.07,
                 duty=0.25, decaimento=9)

        # bateria
        for tempo in range(4):
            kick(buf, t0 + tempo * passo * 4, 0.75)
            if tempo % 2 == 1:
                caixa(buf, t0 + tempo * passo * 4, 0.45)
        for i in range(16):
            chimbal(buf, t0 + i * passo, 0.16 if i % 2 == 0 else 0.09)

        # melodia
        mel = (melodia_a if c < 4 else melodia_b)[c % 4]
        for i, m in enumerate(mel):
            if m is not None:
                nota(buf, t0 + i * passo * 2, passo * 1.9, m, "quadrada",
                     0.20, duty=0.5, decaimento=4)

    buf = eco(buf, passo * 3, 0.4, 0.22)
    salvar("musica_jogo", normalizar(buf, 0.85))


def musica_boss():
    bpm = 164
    passo = 60 / bpm / 4
    compasso = passo * 16
    total = compasso * 8
    buf = np.zeros(int(total * SR))

    prog = [
        (38, MENOR, [74, 74, None, 77, 74, None, 81, 79]),   # Dm
        (34, MAIOR, [70, 70, None, 74, 70, None, 77, 75]),   # Bb
        (36, MAIOR, [72, 72, None, 76, 72, None, 79, 77]),   # C
        (33, MAIOR, [73, 73, None, 76, 73, None, 80, 81]),   # A
    ]

    for c in range(8):
        raiz, tipo, riff = prog[c % 4]
        t0 = c * compasso

        # baixo serrilhado em colcheias
        for i in range(8):
            nota(buf, t0 + i * passo * 2, passo * 1.7, raiz + 12,
                 "serra", 0.28, decaimento=5)

        # arpejo agressivo em semicolcheias
        padrao = [0, 2, 1, 2]
        for i in range(16):
            nota(buf, t0 + i * passo, passo * 0.8,
                 raiz + 24 + tipo[padrao[i % 4]], "quadrada", 0.06,
                 duty=0.125, decaimento=12)

        # bateria pesada: bumbo em todas as semínimas + contratempo
        for tempo in range(4):
            kick(buf, t0 + tempo * passo * 4, 0.85)
            kick(buf, t0 + tempo * passo * 4 + passo * 2.5, 0.5) \
                if tempo % 2 == 0 else None
            if tempo % 2 == 1:
                caixa(buf, t0 + tempo * passo * 4, 0.55)
        for i in range(16):
            chimbal(buf, t0 + i * passo, 0.2)

        # riff (na 2ª metade dobra com oitava acima)
        for i, m in enumerate(riff):
            if m is not None:
                nota(buf, t0 + i * passo * 2, passo * 1.6, m, "quadrada",
                     0.22, duty=0.5, decaimento=7)
                if c >= 4:
                    nota(buf, t0 + i * passo * 2, passo * 1.6, m + 12,
                         "quadrada", 0.08, duty=0.25, decaimento=7)

    buf = eco(buf, passo * 2, 0.35, 0.18)
    salvar("musica_boss", normalizar(buf, 0.85))


# =========================================
# EFEITOS SONOROS
# =========================================

def sfx(nome, dur, funcao, vol=0.8):
    n = int(dur * SR)
    t = np.arange(n) / SR
    salvar(nome, normalizar(funcao(t, n), vol))


def fx_tiro(t, n):
    f = 1100 * np.exp(-t * 14) + 260
    return onda("quadrada", f, t, 0.25) * np.exp(-t * 22)


def fx_explosao(t, n):
    r = passa_baixa(ruido(n), 14) * 4
    corpo = onda("seno", 120 * np.exp(-t * 6) + 35, t)
    return (r * 0.8 + corpo) * np.exp(-t * 6.5)


def fx_dano(t, n):
    f = 340 * np.exp(-t * 5) + 70
    s = onda("serra", f, t) * 0.7 + ruido(n) * 0.35
    return s * np.exp(-t * 7)


def fx_powerup(t, n):
    notas = [72, 76, 79, 84, 88]
    s = np.zeros(n)
    for i, m in enumerate(notas):
        i0 = int(i * 0.06 * SR)
        seg = t[: n - i0]
        s[i0:] += onda("quadrada", hz(m), seg, 0.25) * np.exp(-seg * 7)
    return s


def fx_vida(t, n):
    s = onda("quadrada", hz(83), t, 0.5) * (t < 0.08)
    s += onda("quadrada", hz(88), t, 0.5) * (t >= 0.08) * np.exp(-(t - 0.08) * 9)
    return s


def fx_escudo(t, n):
    f = 300 + 700 * (t / t[-1]) + 25 * np.sin(2 * np.pi * 18 * t)
    return onda("triangulo", f, t) * np.sin(np.pi * t / t[-1]) ** 0.7


def fx_escudo_hit(t, n):
    return (onda("seno", 1500, t) + 0.5 * onda("seno", 2250, t)) * np.exp(-t * 35)


def fx_boss_entra(t, n):
    sirene = 160 + 90 * np.sin(2 * np.pi * 2.2 * t)
    grave = onda("serra", sirene, t) * 0.55
    ronco = onda("quadrada", 45 + 8 * np.sin(2 * np.pi * 7 * t), t) * 0.5
    r = passa_baixa(ruido(n), 10) * 0.8
    env = np.minimum(1, t / 0.1) * np.minimum(1, (t[-1] - t) / 0.35)
    return (grave + ronco + r) * env


def fx_boss_hit(t, n):
    return (onda("seno", 220 * np.exp(-t * 20) + 70, t) * 0.9
            + passa_baixa(ruido(n), 5) * 0.6) * np.exp(-t * 30)


def fx_boss_tiro(t, n):
    f = 380 + 450 * (t / t[-1])
    return onda("seno", f, t) * np.exp(-t * 9)


def fx_vitoria(t, n):
    seq = [(72, 0.0, 0.14), (72, 0.16, 0.14), (72, 0.32, 0.14),
           (72, 0.48, 0.30), (68, 0.80, 0.30), (70, 1.12, 0.30),
           (72, 1.44, 0.18), (70, 1.64, 0.10), (72, 1.78, 1.0)]
    s = np.zeros(n)
    for m, ini, dur in seq:
        i0 = int(ini * SR)
        k = min(int(dur * SR), n - i0)
        if k <= 0:
            continue
        seg = t[:k]
        e = envelope(k, 0.005, 2.5, 0.03)
        s[i0:i0 + k] += onda("quadrada", hz(m + 12), seg, 0.5) * e * 0.5
        s[i0:i0 + k] += onda("triangulo", hz(m), seg) * e * 0.6
    return s


def fx_game_over(t, n):
    seq = [(67, 0.0, 0.35), (64, 0.38, 0.35), (60, 0.76, 0.35),
           (55, 1.14, 1.2)]
    s = np.zeros(n)
    for m, ini, dur in seq:
        i0 = int(ini * SR)
        k = min(int(dur * SR), n - i0)
        seg = t[:k]
        e = envelope(k, 0.01, 2.2, 0.05)
        s[i0:i0 + k] += onda("triangulo", hz(m), seg) * e
        s[i0:i0 + k] += onda("quadrada", hz(m - 12), seg, 0.25) * e * 0.4
    return s


def fx_clique(t, n):
    return onda("quadrada", 880, t, 0.5) * np.exp(-t * 60)


def fx_boss_derrotado(t, n):
    r = passa_baixa(ruido(n), 18) * 4
    corpo = onda("seno", 90 * np.exp(-t * 2.2) + 30, t)
    return (r * 0.9 + corpo) * np.exp(-t * 2.6)


def main():
    musica_menu()
    musica_jogo()
    musica_boss()

    sfx("tiro", 0.14, fx_tiro, 0.55)
    sfx("explosao", 0.55, fx_explosao, 0.85)
    sfx("dano", 0.40, fx_dano, 0.85)
    sfx("powerup", 0.45, fx_powerup, 0.6)
    sfx("vida", 0.40, fx_vida, 0.6)
    sfx("escudo", 0.50, fx_escudo, 0.7)
    sfx("escudo_hit", 0.20, fx_escudo_hit, 0.6)
    sfx("boss_entra", 1.80, fx_boss_entra, 0.85)
    sfx("boss_hit", 0.16, fx_boss_hit, 0.7)
    sfx("boss_tiro", 0.22, fx_boss_tiro, 0.45)
    sfx("boss_derrotado", 1.60, fx_boss_derrotado, 0.9)
    sfx("vitoria", 2.80, fx_vitoria, 0.8)
    sfx("game_over", 2.40, fx_game_over, 0.8)
    sfx("clique", 0.07, fx_clique, 0.5)


if __name__ == "__main__":
    main()
