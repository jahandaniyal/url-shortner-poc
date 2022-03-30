import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """
    Manager class for User Model.
    """
    def create_user(self, name, password=None):
        """
        Create and return a `User` with an username and password.
        """
        if not name:
            raise ValueError('Users Must Have a name')

        user = self.model(
            name=name,
        )
        user.set_password(password)
        print(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):
    """
    The class representing the schema of the User table.
    :param name (Characters): Name of the user.
    :param password (Characters): Password of the user.
    :param is_staff (Number): 1 if the user has admin access else 0.
    :param is_superuser (Number): 1 if the user has admin access else 0.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    last_login = None

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.name

    def has_perm(self):
        return self.is_superuser

    def has_module_perms(self):
        return self.is_superuser