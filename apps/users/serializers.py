from rest_framework import serializers
from .models import User
from ..posts.models import Post
from ..posts.serializers import PostSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя."""
    password = serializers.CharField(write_only=True, min_length=9)
    password2 = serializers.CharField(write_only=True, min_length=9)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, data):
        """Проверяем, что оба пароля совпадают."""
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class UserDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о пользователе."""

    # Добавляем новое поле для постов
    posts_by_country = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'gender',
            'profile_picture',
            'date_of_birth',
            'country',
            'website',
            'phone_number',
            'travel_preferences',
            'languages_spoken',
            'followers_count',
            'notifications_enabled',
            'posts_by_country',  # Добавлено новое поле
        )

    def get_posts_by_country(self, user):
        """
        Получаем посты пользователя, сгруппированные по странам.
        """
        # Получаем посты пользователя, используя обратную связь
        print(f"Получаем посты для пользователя: {user.username} (ID: {user.id})")  # Отладка
        posts = user.posts.select_related('country').all()  # Извлекаем все посты
        print(f"Посты получены: {list(posts)}")  # Отладка, показываем все посты

        grouped_posts = {}

        # Если нет постов, возвращаем пустой словарь
        if not posts.exists():
            print("Нет постов у пользователя. Возвращаем пустой словарь.")  # Отладка
            return grouped_posts

        for post in posts:
            print(f"Обрабатываем пост: {post.title} (ID: {post.id})")  # Отладка
            country_name = post.country.name if post.country else "Без страны"
            print(f"Страна поста: {country_name}")  # Отладка

            if country_name not in grouped_posts:
                grouped_posts[country_name] = []

            # Сериализуем пост и добавляем в группу
            serialized_post = PostSerializer(post).data
            print(f"Сериализованный пост: {serialized_post}")  # Отладка
            grouped_posts[country_name].append(serialized_post)

        print(f"Группировка постов по странам завершена: {grouped_posts}")  # Отладка
        return grouped_posts



class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления информации о пользователе."""
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'gender',
            'profile_picture',
            'date_of_birth',
            'country',
            'website',
            'phone_number',
            'travel_preferences',
            'languages_spoken',
        )


class UserLoginSerializer(serializers.Serializer):
    """Сериализатор для входа пользователя."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserLoginResponseSerializer(serializers.Serializer):
    """Сериализатор для ответа на запрос входа."""
    refresh_token = serializers.CharField()
    access_token = serializers.CharField()
    user_id = serializers.IntegerField()


class LogoutSerializer(serializers.Serializer):
    """Сериализатор для выхода пользователя."""
    refresh_token = serializers.CharField()
