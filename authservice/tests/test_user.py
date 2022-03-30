import json
import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tests.helpers import create_user, get_user


@pytest.mark.django_db
class TestUsers:

    def test_register(self):
        client = APIClient()
        url = reverse('auth_register')
        response = client.post(url, data={"name": "Danny", "password": "123abc@#$"})
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_all_users(self, api_client_admin):
        client = APIClient()
        url_register = reverse('auth_register')
        client.post(url_register, data={"name": "Penny", "password": "123abc@#$"})
        client.post(url_register, data={"name": "Sheldon", "password": "123abc@#$"})
        client.post(url_register, data={"name": "Howard", "password": "123abc@#$"})

        url_get = reverse('users')
        response = api_client_admin.get(url_get)
        assert len(response.data['users']) == 4

    def test_get_user(self):
        api_client, user_id = create_user('Penny')
        url = reverse('user', args=[user_id.id.hex])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_wrong_user(self):
        api_client1, user_id1 = create_user('Penny')
        url = reverse('user', args=[user_id1.id.hex])

        api_client2, user_id2 = create_user('Sheldon')

        response = api_client2.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_user(self):
        api_client_1, user_id_1 = create_user('Penny')
        url = reverse('user', args=[user_id_1.id.hex])

        data = {"name": "Howard"}
        response = api_client_1.put(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == status.HTTP_200_OK

        api_client_2, user_id_2 = get_user("Howard")
        assert user_id_1.id == user_id_2.id

    def test_wrong_user(self):
        api_client_1, user_id_1 = create_user('Penny')
        api_client_2, user_id_2 = create_user('Howard')

        url = reverse('user', args=[user_id_1.id.hex])

        data = {"name": "Sheldon"}
        response = api_client_2.put(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_user_admin(self, api_client_admin):
        api_client, user_id = create_user('Penny')
        url = reverse('user', args=[user_id.id.hex])
        response = api_client_admin.delete(url)
        assert response.status_code == status.HTTP_200_OK

    def test_delete_user(self):
        api_client, user_id = create_user('Penny')
        url = reverse('user', args=[user_id.id.hex])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_200_OK

    def test_delete_wrong_user(self):
        api_client_1, user_id_1 = create_user('Penny')
        api_client_2, user_id_2 = create_user('Howard')

        url = reverse('user', args=[user_id_1.id.hex])

        response = api_client_2.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
