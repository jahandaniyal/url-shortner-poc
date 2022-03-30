# -*- coding: utf-8 -*-

from django.urls import path, re_path

from app import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('user/', views.UsersAPIView.as_view(), name='users'),
    re_path(r'user/(?P<user_id>[^/]+)$', views.UserAPIView.as_view(), name='user'),
    path('shortenurl/', views.ShortUrlAPIView.as_view(), name='shorturl'),
]