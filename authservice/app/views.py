# -*- coding: utf-8 -*-

import json
import requests

from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated
)
from rest_framework.response import Response

from .authentication import AuthorAndAllAdmins
from .controller import (
    delete_user,
    get_all_users,
    get_user_name_by_id,
    update_user
)
from .models import User
from .serializers import UserSerializer
from .utils import sanitize_json_input


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class UsersAPIView(RetrieveAPIView):
    permission_classes = (IsAdminUser, )
    serializer_class = UserSerializer

    def get(self, request):
        users = get_all_users()
        return Response(users)


class UserAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, AuthorAndAllAdmins)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, user_id):
        user_name = get_user_name_by_id(user_id)
        content = {'user is': user_name}
        return Response(content)

    @sanitize_json_input
    def put(self, request, *args, **kwargs):

        data = json.loads(self.request.body)
        uuid = kwargs.get('user_id')
        user_name = update_user(request, data, uuid)
        content = {'user {} has been updated'.format(self.request.user.name): user_name}
        return Response(content)

    def delete(self, request, *args, **kwargs):
        user_name = get_user_name_by_id(kwargs.get('user_id'))
        delete_user(kwargs.get('user_id'))
        content = 'User {} has been deleted'.format(user_name)
        return Response(content)


class ShortUrlAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def get(self, request):
        payload = request.data
        response = requests.post("http://url_service:5000/shortenurl", json=payload).json()
        response['url'] = response['url'].replace('url_service', 'localhost')
        return Response(response)
