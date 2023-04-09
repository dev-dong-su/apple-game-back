"""apple_game_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apple_game.views import EndGameAPIView, StartGameAPIView, SaladLabCreateAPIView, SaladLabUpdateAPIView, SaladLabListAPIView, CheckJWTokenAPIView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('user/all/', SaladLabListAPIView.as_view(), name='user-list'),
    path('user/add/', SaladLabCreateAPIView.as_view(), name='user_add'),
    path('user/update/', SaladLabUpdateAPIView.as_view(), name='user_update'),
    path('user/user_token/', CheckJWTokenAPIView.as_view(), name="user_token"),

    path("game/start/", StartGameAPIView.as_view(), name="start_game"),
    path("game/end/", EndGameAPIView.as_view(), name='end_game')
]
