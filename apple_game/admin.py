from django.contrib import admin
from .models import Saladlab, GameSession


class SaladlabAdmin(admin.ModelAdmin):
    list_display = ('username', 'best_score')
    ordering = ('-best_score',)


class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'is_completed')
    ordering = ('user',)


admin.site.register(Saladlab, SaladlabAdmin)
admin.site.register(GameSession, GameSessionAdmin)
