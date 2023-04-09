from datetime import datetime, timedelta, timezone
import os
import jwt
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header


from .models import GameSession, SaladLab
from .serializers import SaladLabSerializer


class TokenAuthentication(BasePermission):

    def has_permission(self, request, view):
        auth_header = get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b'bearer':
            raise AuthenticationFailed({"message": "토큰이 올바르지 않습니다!"})

        try:
            token = auth_header[1]
            decoded_token = jwt.decode(token, os.getenv(
                'SECRET_KEY'), algorithms='HS256')

        except jwt.InvalidTokenError:
            raise AuthenticationFailed({"message": "토큰이 올바르지 않습니다!"})

        return True


class CheckJWTokenAPIView(APIView):
    permission_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        return Response({"message": "토큰을 검사합니다!"})


class SaladLabCreateAPIView(APIView):
    serializer_class = SaladLabSerializer

    def post(self, request, *args, **kwargs):
        update_data = request.data
        username = update_data.get('username')

        existing_user = SaladLab.objects.filter(username=username).first()
        if existing_user:
            try:
                access_token = jwt.encode(
                    {'username': existing_user.username, 'best_score': existing_user.best_score}, os.getenv('SECRET_KEY'), algorithm='HS256')
                return Response(access_token, status=status.HTTP_200_OK)
            except jwt.InvalidTokenError:
                raise exceptions.AuthenticationFailed('Invalid access token')

        serializer = self.serializer_class(data=update_data)

        if serializer.is_valid():
            user = serializer.save()

            access_token = jwt.encode(
                {'username': user.username, 'best_score': user.best_score}, os.getenv('SECRET_KEY'), algorithm='HS256')
            return Response(access_token, status=status.HTTP_201_CREATED)
        return Response({"message": "토큰이 올바르지 않습니다!", 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SaladLabUpdateAPIView(APIView):
    serializer_class = SaladLabSerializer
    permission_classes = [TokenAuthentication]

    def put(self, request, *args, **kwargs):
        update_data = request.data
        username = update_data.get('username')
        best_score = update_data.get('best_score')
        new_name = update_data.get('new_name', None)
        user = get_object_or_404(SaladLab, username=username)

        if best_score != user.best_score:
            return Response({"message": "유저가 존재하지 않습니다.", 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        if new_name is not None:
            update_data['username'] = new_name

        serializer = self.serializer_class(
            user, data=update_data, partial=True)

        if serializer.is_valid():
            serializer.save()

            access_token = jwt.encode({'username': new_name if new_name else username,
                                      'best_score': best_score}, os.getenv('SECRET_KEY'), algorithm='HS256')
            return Response(access_token, status=status.HTTP_200_OK)
        return Response({"message": "유저 정보를 업데이트 하는데 실패 했습니다!", 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SaladLabListAPIView(ListAPIView):
    queryset = SaladLab.objects.filter(best_score__isnull=False)
    serializer_class = SaladLabSerializer


class StartGameAPIView(APIView):
    permission_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        auth_header = get_authorization_header(request).split()
        token = auth_header[1]
        decoded_token = jwt.decode(token, os.getenv(
            'SECRET_KEY'), algorithms='HS256')
        username = decoded_token['username']

        user = get_object_or_404(SaladLab, username=username)
        game_session = start_game(user)

        return Response({"message": "게임 시작!", "session_id": game_session.id}, status=status.HTTP_200_OK)


class EndGameAPIView(APIView):
    permission_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        auth_header = get_authorization_header(request).split()
        token = auth_header[1]
        decoded_token = jwt.decode(token, os.getenv(
            'SECRET_KEY'), algorithms='HS256')
        username = decoded_token['username']

        user = get_object_or_404(SaladLab, username=username)
        session_id = request.data.get('session_id')
        new_score = request.data.get('new_score')

        game_session = get_object_or_404(GameSession, id=session_id, user=user)

        time_difference = datetime.now(timezone.utc) - game_session.start_time
        if time_difference < timedelta(minutes=2) or time_difference > timedelta(minutes=2, seconds=2):
            return Response({"message": "게임이 비정상적으로 종료 되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

        end_game(game_session, new_score)

        return Response({"message": "게임 종료! 업데이트 완료!"}, status=status.HTTP_200_OK)


def start_game(user):
    game_session = GameSession(user=user)
    game_session.save()
    return game_session


def end_game(game_session, new_score):
    game_session.end_time = datetime.now(timezone.utc)
    game_session.is_completed = True
    game_session.score = new_score
    game_session.save()

    user = game_session.user
    if user.best_score is None or new_score > user.best_score:
        user.best_score = new_score
        user.save()
