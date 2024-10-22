from django.db.models import Sum, Count


class DashboardService:
    def __init__(self, post_model, user_model, tag_model):
        self.post_model = post_model
        self.user_model = user_model
        self.tag_model = tag_model

    def get_latest_posts(self):
        """Получить последние три поста."""
        return self.post_model.objects.order_by('-created_at')[:3]

    def get_top_users(self):
        """Получить топ-5 пользователей с наибольшим количеством лайков постов."""
        return self.user_model.objects.annotate(
            total_likes=Sum('posts__likes')
        ).order_by('-total_likes')[:5]

    def get_tag_cloud(self):
        """Получить облако тегов (с их количеством)."""
        return self.tag_model.objects.annotate(
            post_count=Count('posts')
        ).order_by('-post_count')
