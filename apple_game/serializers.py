from rest_framework import serializers
from .models import SaladLab, GameSession


class SaladLabSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaladLab
        fields = ['username', 'best_score', 'created_at']
