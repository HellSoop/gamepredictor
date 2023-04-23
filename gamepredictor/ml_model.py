import sqlite3
import pandas as pd
import pathlib
from sklearn.neighbors import BallTree
# Файл создаёт модель на основе таблицы из базы данных, а потом упаковывает её.
db_dir = pathlib.Path(__file__).resolve().parent.parent
con = sqlite3.connect(str(db_dir) + '/' + 'db.sqlite3')

games = pd.read_sql('select * from gamepredictor_games', con)  # Создание и заполнение модели
max_k = len(games)  # Нужен будет в ml_utils для избежания ошибок
games_iloc = games.iloc()
X = [g.drop(['id', 'name', 'cover', 'slug']) for g in games_iloc]
tree = BallTree(X, leaf_size=8)


def update_model():
    global games, max_k, games_iloc, X, tree

    con = sqlite3.connect(str(db_dir) + '/' + 'db.sqlite3')
    games = pd.read_sql('select * from gamepredictor_games', con)
    max_k = len(games)
    games_iloc = games.iloc()
    X = [g.drop(['id', 'name', 'cover', 'slug']) for g in games_iloc]
    tree = BallTree(X, leaf_size=8)
