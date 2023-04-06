from django.db import models
from django.utils import timezone


class SaladLab(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10, unique=True)
    best_score = models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-best_score']
