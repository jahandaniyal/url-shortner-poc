import pytest

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


@pytest.mark.django_db
class TestJWT:

    def test_access_token(self, superuser):
        access_token = AccessToken.for_user(superuser)
        assert access_token

    def test_refresh_token(self, superuser):
        refresh = RefreshToken.for_user(superuser)
        assert refresh.access_token