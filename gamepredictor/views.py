from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, CreateView
from django.contrib.auth.views import LoginView

from .models import *
from .forms import *
from . import ml_utils


rep_counter = ml_utils.ReportCounter(10)  # Создание обработчика оценок, назначение длины очереди


class HomeView(TemplateView):
    template_name = 'gamepredictor/choose_games.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        get_games = self.request.GET.get('g') if self.request.GET.get('g') is not None else ''
        games = []
        if get_games:
            for t in set(get_games.split(',')):
                games += Games.objects.filter(name=t)
        previous = '#'
        if self.request.user.is_authenticated:
            previous_games_titles = [g.name for g in self.request.user.gameuserextension.previous_input.all()]
            previous = ','.join(previous_games_titles)
        return {'title': 'Главная страница', 'get_g': get_games, 'games': games, 'previous': previous}


def get_user_interests(games_titles, user):
    '''Не является представлением. Инкапсулирует выбор игр из базы по интересам пользователя.'''
    # Получение точек интересов пользователей
    games = [Games.objects.get(name=g) for g in games_titles]
    ids = [g.id for g in games]
    try:
        ids += [g.id for g in user.gameuserextension.reported_games.all()]
    except AttributeError:
        pass
    users_interests = ml_utils.get_interest_points(games)
    predicted_games = ml_utils.get_closest(users_interests, 3 + len(ids))
    # Поиск игр по id в базе данных и фильтрация результата по id
    res_games = [Games.objects.get(pk=g) for g in predicted_games if g not in ids][:3]

    return res_games


class ResultView(TemplateView):
    template_name = 'gamepredictor/result_games.html'
    result_counter = 0
    check_delay = 25

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.GET.get('g') == '':
            raise Http404

        ResultView.result_counter += 1
        if ResultView.result_counter >= ResultView.check_delay:
            # Если игры с большим id нет, значит модель актуальна
            try:
                Games.objects.get(pk__gt=ml_utils.games_iloc[-1].id)
                ml_utils.update_model()
                ResultView.result_counter = 0
            except Games.DoesNotExist:
                pass

        games_titles = set(self.request.GET.get('g').split(','))  #
        games = get_user_interests(games_titles, self.request.user)

        if self.request.user.is_authenticated:  # Сохранение ввода пользователя
            self.request.user.gameuserextension.previous_input.clear()
            self.request.user.gameuserextension.previous_input.add(*[Games.objects.get(name=g) for g in games_titles])
        return {'title': 'Результаты', 'games': games}


def search_view(request):
    '''Представление. Используется для реализации живого поиска.'''
    q = request.GET.get('q')
    if not q:
        raise Http404
    games = request.GET.get('g')
    titles = Games.objects.filter(name__iregex=q)[:4]
    return render(request, 'gamepredictor/search-help.html', context={'titles': titles, 'games': games})


class ReportView(LoginRequiredMixin, FormView):
    form_class = ReportForm
    template_name = 'gamepredictor/report.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Вызовет ошибку 404, если игры нет в базе данных
        game = get_object_or_404(Games, slug=self.kwargs['game_slug'])
        if game in self.request.user.gameuserextension.reported_games.all():
            raise Http404  # Вызовет ошибку 404, если обработчик не внёс предыдущий результат в базу данных
        return context | {'title': 'Не понравилась игра'}

    def form_valid(self, form):
        game = Games.objects.get(slug=self.kwargs['game_slug'])
        self.request.user.gameuserextension.reported_games.add(game)
        # Помещает данные в обработчик репортов
        rep_counter.put_to_queue({'obj': game, 'values': form.cleaned_data, 'user': self.request.user})
        return redirect('home')


class RegisterUser(CreateView):
    form_class = RegiserForm
    template_name = 'gamepredictor/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context | {'title': 'Регистрация'}

    def form_valid(self, form):
        user = form.save()
        GameUserExtension.objects.create(user=user)
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'gamepredictor/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context | {'title': 'Вход'}

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
