from .ml_model import tree, games_iloc, max_k, update_model


def get_interest_points(games_list: list) -> list:
    games_characteristics_list = []
    for game in games_list:
        games_characteristics_list.append([game.shooter, game.rpg, game.story, game.gloominess, game.aesthetics,
                                           game.survival, game.fullness_of_world, game.creative_potential,
                                           game.fighting_system, game.puzzles, game.quests, game.difficulty,
                                           game.moral, game.horror, game.action, game.emotionality, game.reality,
                                           game.atmosphere])  # вычисление всех характеристик игры
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
    games = [games_iloc[i] for i in ind[0]]  # нахождение игр в датафрейме
    res = [g[1] for g in games]
    return res  # Возврат названий игр
