from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from apps.countries.models import Country
from apps.posts.models import Tag
from apps.users.models import User
from apps.users.serializers import (
    UserDetailSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserLoginResponseSerializer, UserSerializer,
)
from apps.users.services.jwt import AuthService
from apps.users.services.user import (
    UserService,
    UserCreatService,
    UserLoginService,
    UserUpdateService,
    ListUserService,
    SubscriptionService,
)


def create_user_service() -> UserService:
    auth_service = AuthService()
    user_create_service = UserCreatService()
    user_login_service = UserLoginService(auth_service)
    user_update_service = UserUpdateService()
    list_service = ListUserService()
    subscription_service_class = SubscriptionService
    return UserService(
        user_create_service,
        user_login_service,
        user_update_service,
        list_service,
        subscription_service_class,
    )


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    swagger_tags = ["User"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = create_user_service()

    def get_serializer_class(self):
        serializer_map = {
            'sign_up': UserRegistrationSerializer,
            'sign_in': UserLoginSerializer,
            'user': UserDetailSerializer,
            'list': UserSerializer,
        }
        return serializer_map.get(self.action, self.serializer_class)

    @swagger_auto_schema(
        operation_description="Creates a new user with the provided data.",
        request_body=UserRegistrationSerializer,
        responses={201: UserDetailSerializer()}
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='sign_up')
    def sign_up(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.user_service.user_create_service.create(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['username'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            password=serializer.validated_data['password']
        )
        return Response(self.get_serializer(user).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="User login.",
        request_body=UserLoginSerializer,
        responses={200: UserLoginResponseSerializer()}
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='sign_in')
    def sign_in(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response_data = self.user_service.user_login_service.execute(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='get',
        operation_description="Retrieves information about the user.",
        responses={200: UserDetailSerializer()}
    )
    @swagger_auto_schema(
        method='patch',
        operation_description="Updates user information with the provided data.",
        request_body=UserDetailSerializer(),
        responses={200: UserDetailSerializer()}
    )
    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated], url_path='')
    def user(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(data=request.data, instance=user)
            serializer.is_valid(raise_exception=True)
            user = self.user_service.update_user(user.id, **serializer.validated_data)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """
        Получить список всех пользователей с количеством постов и стран.
        """
        users = self.user_service.list_users_with_post_and_country_count()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = create_user_service()

    @swagger_auto_schema(
        operation_description="Подписаться на пользователя.",
    )
    def subscribe_to_user(self, request, pk=None):
        target_user = get_object_or_404(User, pk=pk)
        self.user_service.subscribe_to_user(request.user, target_user)
        return Response({"detail": "Successfully subscribed."}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Отписаться от пользователя.",
    )
    def unsubscribe_from_user(self, request, pk=None):
        target_user = get_object_or_404(User, pk=pk)
        self.user_service.unsubscribe_from_user(request.user, target_user)
        return Response({"detail": "Successfully unsubscribed."}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Подписаться на страну.",
    )
    def subscribe_to_country(self, request, country_id=None):
        country = get_object_or_404(Country, pk=country_id)
        self.user_service.subscribe_to_country(request.user, country)
        return Response({"detail": "Successfully subscribed to country."}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Отписаться от страны.",
    )
    def unsubscribe_from_country(self, request, country_id=None):
        country = get_object_or_404(Country, pk=country_id)
        self.user_service.unsubscribe_from_country(request.user, country)
        return Response({"detail": "Successfully unsubscribed from country."}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Подписаться на тег.",

    )
    def subscribe_to_tag(self, request, tag_id=None):
        tag = get_object_or_404(Tag, pk=tag_id)
        self.user_service.subscribe_to_tag(request.user, tag)
        return Response({"detail": "Successfully subscribed to tag."}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Отписаться от тега.",
    )
    def unsubscribe_from_tag(self, request, tag_id=None):
        tag = get_object_or_404(Tag, pk=tag_id)
        self.user_service.unsubscribe_from_tag(request.user, tag)
        return Response({"detail": "Successfully unsubscribed from tag."}, status=status.HTTP_200_OK)
