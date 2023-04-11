from django.contrib import admin
from .models import SaladLab, GameSession


class SaladLabAdmin(admin.ModelAdmin):
    list_display = ('username', 'best_score')
    ordering = ('-best_score',)


class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'is_completed', 'start_time')
    ordering = ('-start_time',)  # start_time을 기준으로 내림차순 정렬
    list_filter = ('is_completed',)  # is_completed 필드를 기준으로 필터링 옵션 추가


admin.site.register(SaladLab, SaladLabAdmin)
admin.site.register(GameSession, GameSessionAdmin)
