from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from apps.users.models import User


class AuthService:
    """
    Service for managing authentication tokens.
    """
    def get_tokens_for_user(self, user: User) -> dict:
        refresh = RefreshToken.for_user(user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}

    def logout(self, refresh_token: str) -> bool:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return True
        except TokenError:
            return False
