from . import models
import pandas as pd
from sklearn.neighbors import BallTree
# Файл создаёт модель на основе таблицы из базы данных, а потом упаковывает её.


def get_games_from_db():
    games_from_db = models.Games.objects.all()
    return pd.DataFrame({  # занонсит все необходимые данныйе в DataFrame
        'id': [game.id for game in games_from_db],
        'shooter': [game.shooter for game in games_from_db],
        'rpg': [game.rpg for game in games_from_db],
        'story': [game.story for game in games_from_db],
        'gloominess': [game.gloominess for game in games_from_db],
        'aesthetics': [game.aesthetics for game in games_from_db],
        'survival': [game.survival for game in games_from_db],
        'fullness_of_world': [game.fullness_of_world for game in games_from_db],
        'creative_potential': [game.creative_potential for game in games_from_db],
        'fighting_system': [game.fighting_system for game in games_from_db],
        'puzzles': [game.puzzles for game in games_from_db],
        'quests': [game.quests for game in games_from_db],
        'difficulty': [game.difficulty for game in games_from_db],
        'moral': [game.moral for game in games_from_db],
        'horror': [game.horror for game in games_from_db],
        'action': [game.action for game in games_from_db],
        'emotionality': [game.emotionality for game in games_from_db],
        'reality': [game.reality for game in games_from_db],
        'atmosphere': [game.atmosphere for game in games_from_db]
    })


games = get_games_from_db()
max_k = len(games)  # Нужен будет в ml_utils для избежания ошибок
games_iloc = games.iloc
X = [g.drop(['id']) for g in games_iloc]
tree = BallTree(X, leaf_size=8)
