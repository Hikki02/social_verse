from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from services.base.pagination import ProductPagination
from .models import PostImage, Post, Tag
from .serializers import PostSerializer, TagSerializer
from .services.dashboard import DashboardService
from .services.posts import PostService
from .services.posts import CreatePostService, UpdatePostService, DeletePostService, ListPostService, RetrievePostService
from ..users.models import User
from ..users.serializers import UserDetailSerializer


def create_post_service() -> PostService:
    create_service = CreatePostService()
    update_service = UpdatePostService()
    delete_service = DeletePostService()
    list_service = ListPostService()
    retrieve_service = RetrievePostService()
    return PostService(create_service, update_service, delete_service, list_service, retrieve_service)


class PostViewSet(viewsets.GenericViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ProductPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.post_service = create_post_service()

    @swagger_auto_schema(
        request_body=PostSerializer,
        responses={201: PostSerializer()},
        operation_description="Создать новый пост."
    )
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        post_data = serializer.validated_data
        images = post_data.pop('images', [])
        post_data['author'] = request.user

        # Создаем пост с использованием сервиса
        post = self.post_service.create_post(**post_data)

        # Обрабатываем изображения
        for image in images:
            PostImage.objects.create(post=post, image=image)

        return Response(self.serializer_class(post).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={200: PostSerializer()},
        operation_description="Получить информацию о конкретном посте.",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="ID поста", type=openapi.TYPE_INTEGER),
        ]
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        post = self.post_service.retrieve_post(pk)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=PostSerializer,
        responses={200: PostSerializer()},
        operation_description="Обновить информацию о посте."
    )
    def update(self, request, pk=None, *args, **kwargs):
        # Получаем пост, который нужно обновить
        post = self.post_service.update_post(pk, **request.data)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={204: openapi.Response("Пост успешно удален")},
        operation_description="Удалить пост по ID."
    )
    def destroy(self, request, pk=None, *args, **kwargs):
        self.post_service.delete_post(pk)
        return Response({"message": "Пост успешно удален"}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        responses={200: PostSerializer(many=True)},
        operation_description="Получить список всех постов с пагинацией."
    )
    def list(self, request, *args, **kwargs):
        """
        Получить список всех постов с пагинацией.
        """
        paginator = self.pagination_class()
        posts = self.post_service.list_posts()

        paginated_posts = paginator.paginate_queryset(posts, request)
        serializer = self.get_serializer(paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    @swagger_auto_schema(
        responses={200: PostSerializer(many=True)},
        operation_description="Получить посты для главной страницы."
    )
    def main_page(self, request):
        paginator = self.pagination_class()

        if request.user.is_authenticated:
            posts = self.post_service.get_posts_for_authenticated_user(request.user)
        else:
            posts = self.post_service.get_posts_for_unauthenticated_user()

        paginated_posts = paginator.paginate_queryset(posts, request)
        serializer = self.get_serializer(paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data)


class DashboardViewSet(viewsets.ViewSet):
    """
    ViewSet для получения данных для блоков последних постов, облака тегов и топ пользователей.
    """
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dashboard_service = DashboardService(Post, User, Tag)

    @swagger_auto_schema(
        operation_description="Возвращает последние посты, облако тегов и топ пользователей."
    )
    def list(self, request):
        """
        Возвращает последние посты, облако тегов и топ пользователей.
        """
        latest_posts = self.dashboard_service.get_latest_posts()
        top_users = self.dashboard_service.get_top_users()
        tag_cloud = self.dashboard_service.get_tag_cloud()

        latest_posts_serializer = PostSerializer(latest_posts, many=True)
        top_users_serializer = UserDetailSerializer(top_users, many=True)
        tag_cloud_serializer = TagSerializer(tag_cloud, many=True)

        # Формируем ответ
        return Response({
            'latest_posts': latest_posts_serializer.data,
            'top_users': top_users_serializer.data,
            'tag_cloud': tag_cloud_serializer.data,
        })
