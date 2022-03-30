# -*- coding: utf-8 -*-

"""Authentication Functions for Users and Admins.
This module implements authentication for all API calls.
There are two auth classes - AuthorAndAllAdmins and, IsAdminOrReadOnly
for different levels of permissions.
"""

from rest_framework import permissions


class AuthorAndAllAdmins(permissions.BasePermission):
    """Allow all access to Admin and Owner of resource.
    Attributes:
        SAFE_METHODS (tuple): Tuple of all permissible HTTP Methods for this Auth Class.
    """
    SAFE_METHODS = ("GET", "PUT", "PATCH", "DELETE", "POST")

    def has_permission(self, request, view):
        """Override has_permission of BasePermission class.
            Returns true if User is Admin, or Owner of Resource.
            Also, checks if request methods is one of the SAFE_METHODS.
            Args:
                request (Object): [Required].
                view (Object): [Required].
            Returns (bool):
                Return `True` if permission is granted, `False` otherwise.
        """
        if request.method not in self.SAFE_METHODS:
            return False

        if request.user.is_superuser:
            return True

        elif view.kwargs.get('user_id') == str(request.user.id):
            return True

        return False


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Allow all access to Admin or only ReadOnly access to other Users
    Attributes:
        SAFE_METHODS (tuple): Tuple of all permissible HTTP Methods for this Auth Class.
    """

    SAFE_METHODS = ("GET", "PUT", "PATCH", "DELETE", "POST")

    def has_permission(self, request, view):
        """Override has_permission of BasePermission class.
            Returns true if User is Authenticated.
            Returns true if HTTP method is GET.
            Also, checks if request methods is one of the SAFE_METHODS.
            Args:
                request (Object): [Required].
                view (Object): [Required].
            Returns (bool):
                Return `True` if permission is granted, `False` otherwise.
        """
        if request.method not in self.SAFE_METHODS:
            return False

        if request.user and request.user.is_authenticated:
            return True

        elif request.method == "GET":
            return True

        return False