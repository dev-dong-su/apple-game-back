from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    password1 = None
    password2 = None
    
    class Meta:
        model = User
        fields = ('username', 'best_score')

    def clean_password2(self):
        return None