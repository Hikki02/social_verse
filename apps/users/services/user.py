from django.db.models import Count
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from apps.users.models import User
from services.base.service import BaseService
from .jwt import AuthService


class UserCreatService(BaseService):
    """
    Сервис для создания пользователей.
    """
    model = User

    @classmethod
    def create(cls, email: str, username: str, first_name: str, last_name: str, password: str) -> User:
        """Создает новый экземпляр пользователя с логикой валидации.

        Args:
            email: Email пользователя.
            username: Имя пользователя.
            first_name: Имя пользователя.
            last_name: Фамилия пользователя.
            password: Пароль пользователя.

        Returns:
            Экземпляр созданного пользователя.

        Raises:
            ValidationError: Если экземпляр не проходит валидацию.
        """
        user = super().create(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        user.set_password(password)
        user.save()
        return user


class UserUpdateService(BaseService):
    model = User


class UserLoginService(BaseService):
    """
    Service for managing user login.
    """

    model = User

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def get_by_email(self, email: str) -> User:
        return get_object_or_404(self.model, email=email)

    @staticmethod
    def _create_response(user_id: int, token_data: dict) -> dict:
        return {
            "access_token": str(token_data['access']),
            "refresh_token": str(token_data['refresh']),
            "user_id": user_id,
        }

    def execute(self, email: str, password: str) -> dict:
        """Executes user login by validating email and password.

        Args:
            email (str): The email of the user.
            password (str): The password provided by the user.

        Returns:
            dict: A dictionary containing access and refresh tokens, and user ID.

        Raises:
            ValueError: If the user is not found or password is incorrect.
        """
        user = self.get_by_email(email)

        if not user.check_password(password):
            raise ValidationError({"password": "Invalid password."}, code=400)

        token_data = self.auth_service.get_tokens_for_user(user)
        return self._create_response(user.id, token_data)


class UserLogoutService:
    """
    Сервис для управления выходом пользователей.
    """

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def execute(self, refresh_token: str) -> bool:
        return self.auth_service.logout(refresh_token)


class ListUserService(BaseService):
    """
    Сервис для получения списка пользователей с дополнительной информацией.
    """
    model = User

    def get_users_with_post_and_country_count(self):
        """
        Возвращает пользователей с количеством постов и количеством стран,
        к которым пользователь создал посты.
        """
        return self.model.objects.annotate(
            post_count=Count('posts'),
            country_count=Count('posts__country', distinct=True)
        )


class SubscriptionService(BaseService):
    model = User

    def __init__(self, user: User):
        self.user = user

    def subscribe_to_user(self, target_user_id: int):
        target_user = get_object_or_404(self.model, id=target_user_id)
        self.user.subscribed_users.add(target_user)
        self.user.save()

    def unsubscribe_from_user(self, target_user_id: int):
        target_user = get_object_or_404(self.model, id=target_user_id)
        self.user.subscribed_users.remove(target_user)
        self.user.save()

    def subscribe_to_country(self, country):
        self.user.subscribed_countries.add(country)
        self.user.save()

    def unsubscribe_from_country(self, country):
        self.user.subscribed_countries.remove(country)
        self.user.save()

    def subscribe_to_tag(self, tag):
        self.user.subscribed_tags.add(tag)
        self.user.save()

    def unsubscribe_from_tag(self, tag):
        self.user.subscribed_tags.remove(tag)
        self.user.save()


class UserService:
    def __init__(self,
                 user_create_service: UserCreatService,
                 user_login_service: UserLoginService,
                 user_update_service: UserUpdateService,
                 list_service: ListUserService,
                 subscription_service_class: type,
                 ):
        self.list_service = list_service
        self.user_create_service = user_create_service
        self.user_login_service = user_login_service
        self.user_update_service = user_update_service
        self.subscription_service_class = subscription_service_class

    def sign_up(self, **kwargs):
        return self.user_create_service.create(**kwargs)

    def sign_in(self, email: str, password: str) -> dict:
        return self.user_login_service.execute(email, password)

    def update_user(self, user_id: int, **kwargs) -> User:
        return self.user_update_service.update(user_id, **kwargs)

    def list_users_with_post_and_country_count(self):
        return self.list_service.get_users_with_post_and_country_count()

    def subscribe_to_user(self, user: User, target_user: User):
        subscription_service = self.subscription_service_class(user)
        subscription_service.subscribe_to_user(target_user)

    def unsubscribe_from_user(self, user: User, target_user: User):
        subscription_service = self.subscription_service_class(user)
        subscription_service.unsubscribe_from_user(target_user)

    def subscribe_to_country(self, user: User, country):
        subscription_service = self.subscription_service_class(user)
        subscription_service.subscribe_to_country(country)

    def unsubscribe_from_country(self, user: User, country):
        subscription_service = self.subscription_service_class(user)
        subscription_service.unsubscribe_from_country(country)

    def subscribe_to_tag(self, user: User, tag):
        subscription_service = self.subscription_service_class(user)
        subscription_service.subscribe_to_tag(tag)

    def unsubscribe_from_tag(self, user: User, tag):
        subscription_service = self.subscription_service_class(user)
        subscription_service.unsubscribe_from_tag(tag)

