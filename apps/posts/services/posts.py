from django.db.models import Q
from django.http import JsonResponse

from apps.posts.models import Post
from apps.users.models import User
from services.base.service import BaseService


class CreatePostService(BaseService):
    """
    Service for creating posts.
    """
    model = Post


class UpdatePostService(BaseService):
    """
    Service for updating posts.
    """
    model = Post


class DeletePostService(BaseService):
    """
    Service for deleting posts.
    """
    model = Post


class ListPostService(BaseService):
    """
    Service for listing posts.
    """
    model = Post

    @staticmethod
    def get_main_page_posts_for_authenticated_user(user):
        """
        Получить посты для авторизованного пользователя, основываясь на его подписках.
        """
        subscribed_users = user.subscribed_users.all()
        subscribed_countries = user.subscribed_countries.all()
        subscribed_tags = user.subscribed_tags.all()

        posts = Post.objects.filter(
            Q(author__in=subscribed_users) |
            Q(country__in=subscribed_countries) |
            Q(tags__in=subscribed_tags)
        ).distinct().order_by('-created_at')

        return posts

    @staticmethod
    def get_main_page_posts_for_unauthenticated_user():
        """
        Получить последние 10 постов для неавторизованного пользователя.
        """
        return Post.objects.all().order_by('-created_at')[:10]


class RetrievePostService(BaseService):
    """
    Service for retrieving a post by ID.
    """
    model = Post


class PostService:
    def __init__(self,
                 create_service: CreatePostService,
                 update_service: UpdatePostService,
                 delete_service: DeletePostService,
                 list_service: ListPostService,
                 retrieve_service: RetrievePostService,
                 ):
        self.create_service = create_service
        self.update_service = update_service
        self.delete_service = delete_service
        self.list_service = list_service
        self.retrieve_service = retrieve_service

    def create_post(self, **kwargs) -> Post:
        return self.create_service.create(**kwargs)

    def update_post(self, post_id: int, **kwargs) -> Post:
        return self.update_service.update(post_id, **kwargs)

    def delete_post(self, post_id: int) -> JsonResponse:
        return self.delete_service.delete(post_id)

    def list_posts(self):
        return self.list_service.get_all()

    def retrieve_post(self, post_id: int):
        return self.retrieve_service.get_by_id(post_id)

    def get_posts_for_authenticated_user(self, user: User):
        return self.list_service.get_main_page_posts_for_authenticated_user(user)

    def get_posts_for_unauthenticated_user(self):
        return self.list_service.get_main_page_posts_for_unauthenticated_user()

