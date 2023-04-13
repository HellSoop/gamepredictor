from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView, CreateView
from django.contrib.auth.views import LoginView

from .models import *
from .forms import *
from . import ml_utils
from . import ml_model


class HomeView(TemplateView):
    template_name = 'gamepredictor/choose_games.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        get_games = self.request.GET.get('g') if self.request.GET.get('g') is not None else ''
        games = []
        if get_games:
            for t in set(get_games.split(',')):
                games += Games.objects.filter(name__iregex=t)
        return {'title': 'Главная страница', 'get_g': get_games, 'games': games}


def get_user_interests(games_titles):
    '''Не является представлением. Инкапсулирует выбор игр из базы по интересам пользователя.'''
    games = [ml_utils.get_characteristics(Games.objects.get(name=g)) for g in games_titles]
    users_interests = []  # предыдущая строка создаёт списко со списками с характеристиками каждой игры в запросе
    for i in range(len(games[0])):
        # вычисление среднего значения каждой харатеритики
        users_interests.append(sum([g[i] for g in games]) / len(games))
    predicted_games = [g for g in ml_utils.get_closest(users_interests, 3 + len(games_titles)) if not g in games_titles][:3]
    res_games = [Games.objects.get(name=g) for g in predicted_games if not g in games_titles]
    # в предыдущей строке по названиям игр ищутся их объекты в базе данных
    return res_games


class ResultView(TemplateView):
    template_name = 'gamepredictor/result_games.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.GET.get('g') == '':
            return Http404
        games_titles = set(self.request.GET.get('g').split(','))
        return {'title': 'Результаты', 'games': get_user_interests(games_titles)}


def search_view(request):
    '''Представление. Используется для реализации живого поиска.'''
    q = request.GET.get('q')
    if not q:
        raise Http404
    games = request.GET.get('g')
    titles = Games.objects.filter(name__iregex=q)[:4]
    return render(request, 'gamepredictor/search-help.html', context={'titles': titles, 'games': games})


def report_view(request, game_slug):
    pass


class ReportView(LoginRequiredMixin, FormView):
    form_class = ReportForm
    template_name = 'gamepredictor/report.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context | {'title': 'Не понравилась игра'}

    def form_valid(self, form):
        print(form.cleaned_data)
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
