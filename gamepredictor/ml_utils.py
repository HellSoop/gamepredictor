from .ml_model import tree, games_iloc, max_k


def get_characteristics(game):
    return [game.shooter, game.rpg, game.story, game.gloominess, game.aesthetics,
                            game.survival, game.fullness_of_world, game.creative_potential,
                            game.fighting_system, game.puzzles, game.quests, game.difficulty,
                            game.moral, game.horror, game.action, game.emotionality, game.reality,
                            game.atmosphere]


def get_closest(game_characteristics, k=3):
    '''Финаальная функция для получения названий игр'''
    if k > max_k:
        k = max_k
    _, ind = tree.query([game_characteristics], k=k)  # нахождение индексов игр
    games = [games_iloc[i] for i in ind[0]]  # нахождение игр в датафрейме
    res = [g[1] for g in games]
    return res  # Возврат названий игр
