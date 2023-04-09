from django.contrib import admin
from .models import SaladLab, GameSession


class SaladLabAdmin(admin.ModelAdmin):
    list_display = ('username', 'best_score')
    ordering = ('-best_score',)


class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'is_completed')
    ordering = ('user',)


admin.site.register(SaladLab, SaladLabAdmin)
admin.site.register(GameSession, GameSessionAdmin)
