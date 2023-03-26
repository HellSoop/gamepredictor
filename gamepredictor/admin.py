from django.contrib import admin
from .models import *
 # Нужно для регистрации кастомной модели пользователей
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class GamepredictorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'cover']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name']


admin.site.register(Games, GamepredictorAdmin)


class UserExtension(admin.StackedInline):
    model = GameUserExtension
    can_delete = False
    verbose_name_plural = 'Пользователи'
    filter_horizontal = ['previous_input', 'reported_games']

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserExtension,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
