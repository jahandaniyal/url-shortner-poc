# -*- coding: utf-8 -*-

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Allows serialisation and deserialisation of `User` model objects.
    Attributes:
        name (CharField): [Required, Write_only].
        password (CharField): [Required, Write_only].
    """
    name = serializers.CharField(write_only=True, required=True)

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('password', 'name')

    def create(self, validated_data):
        """
        Create and return a `User` with an username and password.
        """
        user = User.objects.create(
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        """
        Update and return updated `User`.
        """
        instance.name = validated_data.get('name', instance.name)

        instance.save()

        return instance
