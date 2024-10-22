from rest_framework import serializers
from .models import Post, PostImage, Tag, Comment


from rest_framework import serializers


class PostImageSerializer(serializers.ModelSerializer):
    """Сериализатор для представления изображений постов."""

    class Meta:
        model = PostImage
        fields = ('id', 'post', 'image')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):

    images = PostImageSerializer(many=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'body', 'country', 'tags', 'images']

    def validate_body(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Содержимое поста должно содержать минимум 3 символа.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для представления информации о комментариях."""

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'body', 'created_at')
