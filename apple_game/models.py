from django.db import models
from django.utils import timezone


class SaladLab(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    best_score = models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-best_score']


class GameSession(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(SaladLab, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.id
