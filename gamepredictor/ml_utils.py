from .ml_model import tree, games_iloc, max_k


def get_interest_points(games_list):
    games_characteristics_list = []
    for game in games_list:
        games_characteristics_list.append([game.shooter, game.rpg, game.story, game.gloominess, game.aesthetics,
                                           game.survival, game.fullness_of_world, game.creative_potential,
                                           game.fighting_system, game.puzzles, game.quests, game.difficulty,
                                           game.moral, game.horror, game.action, game.emotionality, game.reality,
                                           game.atmosphere])
    for i in range(len(games_characteristics_list[0])):
        all_values = list(sorted(enumerate([game[i] for game in games_characteristics_list])))
    return games_characteristics_list


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


def get_closest(game_characteristics, k=3):
    '''Финаальная функция для получения названий игр'''
    if k > max_k:
        k = max_k
    _, ind = tree.query([game_characteristics], k=k)  # нахождение индексов игр
    games = [games_iloc[i] for i in ind[0]]  # нахождение игр в датафрейме
    res = [g[1] for g in games]
    return res  # Возврат названий игр
