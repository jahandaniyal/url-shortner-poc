# -*- coding: utf-8 -*-

"""Controller Functions for all database operations.
This module provides helper functions for the following operations:
    1. Creation
    2. Deletion
    3. Updation
    4. Deletion
The operations apply to the following models:
    1. User
    2. Usage
    3. UsageTypes
Todo:
    * Adding Logging
"""
from rest_framework.exceptions import PermissionDenied

from .models import User


def create_user(data):
    """Create a new user and save it in the database.
        Args:
            data (dict): {'name': <string>, 'password': <string>}.
                input data required for User creation
        Returns (None):
            None.
    """
    user = User(name=data.get('name'))
    user.save()


def delete_user(user_id):
    """Delete a User from the database.
        Args:
            user_id (string): [Required].
        Returns (None):
            None.
    """
    User.objects.get(pk=user_id).delete()


def get_all_users():
    """Get all Users from the database.
        Args:
            None.
        Returns (dict):
            Returns a dict containing list of Users.
    """
    users = User.objects.all()
    users_data = [{"id": user.id.hex, "name": user.name} for user in users]
    return {'users' : users_data}


def get_user_name_by_id(user_id):
    """Get User name from the database using user_id.
        Args:
            user_id (string): [Required].
        Returns (dict):
            Returns user name of the User matching user_id.
    """
    user = User.objects.get(pk=user_id)
    return user.name


def get_user_id_by_name(name):
    """Get User ID from the database using name of the User.
        Args:
            name (string): [Required].
        Returns (dict):
            Returns User ID of the User matching username.
    """
    user = User.objects.get(name=name)
    return user.id


def update_user(request, data, user_id):
    """Update User in the database using User ID.
        Args:
            request (Request): [Required].
            data (dict): [Required].
            user_id (string): [Required].
        Returns (dict):
            Returns User name of the updated User.
    """
    if request.user.id.hex != user_id:
        raise PermissionDenied

    user = User.objects.get(pk=user_id)
    user.name = data.get('name')
    user.save()
    return user.name
