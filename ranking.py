
import sqlite3
from pathlib import Path
from datetime import datetime


# Caminho do banco de dados
BASE_DIR = Path(__file__).resolve().parent.parent

PASTA_DATABASE = BASE_DIR / "database"

PASTA_DATABASE.mkdir(exist_ok=True)

DB_PATH = PASTA_DATABASE / "records.db"


def conectar():
    return sqlite3.connect(DB_PATH)


def inicializar_banco():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jogadores (
            id_jogador INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE COLLATE NOCASE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id_recorde INTEGER PRIMARY KEY AUTOINCREMENT,
            id_jogador INTEGER NOT NULL,
            pontuacao INTEGER NOT NULL,
            resultado TEXT NOT NULL,
            tempo_gasto INTEGER NOT NULL,
            data_registro TEXT NOT NULL,

            FOREIGN KEY (id_jogador)
            REFERENCES jogadores(id_jogador)
        )
    """)

    conexao.commit()
    conexao.close()


def registrar_jogador(login):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO jogadores (login)
        VALUES (?)
    """, (login,))

    conexao.commit()

    cursor.execute("""
        SELECT id_jogador
        FROM jogadores
        WHERE login = ?
    """, (login,))

    jogador = cursor.fetchone()

    conexao.close()

    return jogador[0]


def salvar_recorde(login, pontuacao, resultado, tempo_gasto):
    conexao = conectar()
    cursor = conexao.cursor()

    id_jogador = registrar_jogador(login)

    data_atual = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO records (
            id_jogador,
            pontuacao,
            resultado,
            tempo_gasto,
            data_registro
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        id_jogador,
        pontuacao,
        resultado,
        tempo_gasto,
        data_atual
    ))

    conexao.commit()
    conexao.close()


def obter_ranking():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            jogadores.login,
            records.pontuacao,
            records.tempo_gasto

        FROM jogadores

        INNER JOIN records
            ON jogadores.id_jogador = records.id_jogador

        WHERE records.id_recorde = (

            SELECT r2.id_recorde

            FROM records AS r2

            WHERE r2.id_jogador = jogadores.id_jogador

            ORDER BY
                r2.pontuacao DESC,
                r2.tempo_gasto ASC,
                r2.data_registro ASC

            LIMIT 1
        )

        ORDER BY
            records.pontuacao DESC,
            records.tempo_gasto ASC

        LIMIT 10;
    """)

    ranking = cursor.fetchall()

    conexao.close()

    return ranking
