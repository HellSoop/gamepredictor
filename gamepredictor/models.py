from django.db import models
from django.contrib.auth.models import User

class Games(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Название игры')
    # характеристики игр
    shooter = models.IntegerField()
    rpg = models.IntegerField()
    story = models.IntegerField()
    gloominess = models.IntegerField()
    aesthetics = models.IntegerField()
    survival = models.IntegerField()
    fullness_of_world = models.IntegerField()
    creative_potential = models.IntegerField()
    fighting_system = models.IntegerField()
    puzzles = models.IntegerField()
    quests = models.IntegerField()
    difficulty = models.IntegerField()
    moral = models.IntegerField()
    horror = models.IntegerField()
    action = models.IntegerField()
    emotionality = models.IntegerField()
    reality = models.IntegerField()
    atmosphere = models.IntegerField()

    cover = models.ImageField(null=True, verbose_name='Обложка')
    slug = models.SlugField(unique=True, db_index=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ['id']

    def __str__(self):
        return self.name


class GameUserExtension(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    previous_input = models.ManyToManyField(Games, blank=True, related_name='previous_input', related_query_name='previous_input') # Предыдущий ввод пользователя
    reported_games = models.ManyToManyField(Games, blank=True, related_name='reported_games', related_query_name='reported_games') # Непонравившиеся игры
