
from rest_framework import serializers
from .models import Country
from ..posts.models import Post
from ..posts.serializers import PostSerializer


class CountrySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ['id', 'name', 'post_count']

    def get_post_count(self, obj):
        return obj.post_set.count()


class CountryDetailSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ['id', 'name', 'posts']

    def get_posts(self, obj):
        posts = Post.objects.filter(country=obj).order_by('-created_at')
        return PostSerializer(posts, many=True).data

