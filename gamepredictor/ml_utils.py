from .ml_model import *


def update_model():
    global games, max_k, games_iloc, X, tree

    games = get_games_from_db()
    max_k = len(games)
    games_iloc = games.iloc
    X = [g.drop(['id']) for g in games_iloc]
    tree = BallTree(X, leaf_size=8)


def get_characteristics(game):
    return [game.shooter, game.rpg, game.story, game.gloominess, game.aesthetics,
            game.survival, game.fullness_of_world, game.creative_potential,
            game.fighting_system, game.puzzles, game.quests, game.difficulty,
            game.moral, game.horror, game.action, game.emotionality, game.reality,
            game.atmosphere]


def get_interest_points(games_list: list) -> list:
    # вычисление всех характеристик игры
    games_characteristics_list = [get_characteristics(game) for game in games_list]
    characteristics_count = len(games_characteristics_list[0])
    l_games = len(games_list)
    games_mean = []  # вычисление среднего значения всех характеристик игр
    for i in range(characteristics_count):
        games_mean.append(sum([g[i] for g in games_characteristics_list]) / l_games)
    max_distance = 75  # максимальное различие в характеристиках точек
    max_center_distance = 50
    res = []  # результирующий список

    for game in games_characteristics_list:
        # Если какое-либо значение отличается от значения у средней точки больше, чем дозволено,
        # создаётся ещё одна точка интересов
        if max([abs(game[i] - games_mean[i]) for i in range(characteristics_count)]) >= max_center_distance:
            corrections = []
            for another_game in games_characteristics_list:
                for i in range(characteristics_count):
                    if abs(another_game[i] - game[i]) >= max_distance:
                        if game[i] > another_game[i]:
                            corrections.append((i, (game[i] - another_game[i]) / l_games))
                        else:
                            corrections.append((i, -1 * (another_game[i] - game[i]) / l_games))
            interest_point = games_mean.copy()
            for i, v in corrections:
                interest_point[i] += v
            res.append(interest_point)
    res.append(games_mean)
    for g in games_characteristics_list:
        if min([abs(g[i] - games_mean[i]) for i in range(characteristics_count)]) < max_center_distance:
            break
    else:
        res.pop()
    return res


class ReportCounter:
    def __init__(self, delay: int):
        self.delay = delay
        self.queue = []

    def put_to_queue(self, obj: dict) -> None:
        self.queue.append(obj)
        print(self.queue)
        if len(self.queue) >= self.delay:
            for item in self.queue:
                game = item['obj']
                for attr, val in item['values'].items():
                    game.__setattr__(attr, game.__getattribute__(attr) + int(val))
                game.save()
                item['user'].gameuserextension.reported_games.remove(game)
            self.queue = []
            update_model()


def get_closest(game_characteristics, k=3):
    '''Финаальная функция для получения названий игр'''
    if k > max_k:
        k = max_k
    _, ind = tree.query(game_characteristics, k=k)  # нахождение индексов игр
    return [games_iloc[i].id for i in ind[0]]  # Возврат id игр
