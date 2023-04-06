import os
import jwt
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import BasePermission
from rest_framework.authentication import get_authorization_header


from .models import SaladLab
from .serializers import SaladLabSerializer


class TokenAuthentication(BasePermission):

    def has_permission(self, request, view):
        auth_header = get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b'bearer':
            return False

        try:
            token = auth_header[1]
            decoded_token = jwt.decode(token, os.getenv(
                'SECRET_KEY'), algorithms='HS256')

        except jwt.InvalidTokenError:
            return False

        return True


class UserCreateAPIView(APIView):
    serializer_class = SaladLabSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')

        existing_user = SaladLab.objects.filter(username=username).first()
        if existing_user:
            try:
                access_token = jwt.encode({'username': existing_user.username, 'best_score': existing_user.best_score}, os.getenv(
                    'SECRET_KEY'), algorithm='HS256')
                return Response(access_token, status=status.HTTP_200_OK)
            except jwt.InvalidTokenError:
                raise exceptions.AuthenticationFailed('Invalid access token')

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user = serializer.save()

            access_token = jwt.encode({'username': user.username, 'best_score': user.best_score}, os.getenv(
                'SECRET_KEY'), algorithm='HS256')
            return Response(access_token, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateAPIView(APIView):
    serializer_class = SaladLabSerializer
    permission_classes = [TokenAuthentication]

    def put(self, request, *args, **kwargs):
        username = request.data.get('username')
        best_score = request.data.get('best_score')
        new_name = request.data.get('new_name', None)
        user = get_object_or_404(SaladLab, username=username)

        update_data = request.data
        if new_name is not None:
            update_data['username'] = new_name

        serializer = self.serializer_class(
            user, data=update_data, partial=True)
        if serializer.is_valid():
            serializer.save()

            access_token = jwt.encode({'username': new_name if new_name else username,
                                      'best_score': best_score}, os.getenv('SECRET_KEY'), algorithm='HS256')
            return Response(access_token, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersListAPIView(ListAPIView):
    queryset = SaladLab.objects.filter(best_score__isnull=False)
    serializer_class = SaladLabSerializer


class CheckJWTokenAPIView(APIView):
    permission_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        return Response({"message": "Token is valid"})
