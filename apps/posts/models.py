from django.db import models
from django.conf import settings

from services.base.models import TimeStampModel


class Post(TimeStampModel):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Содержимое")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор", related_name='posts')
    country = models.ForeignKey('countries.Country', on_delete=models.SET_NULL, null=True, verbose_name="Страна")
    tags = models.ManyToManyField('Tag', blank=True, verbose_name="Теги", related_name='posts')
    likes = models.PositiveIntegerField(default=0, verbose_name="Количество лайков")

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.title


class PostImage(TimeStampModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name="Пост")
    image = models.ImageField(upload_to='post_images/', verbose_name="Изображение")

    class Meta:
        verbose_name = "Изображение поста"
        verbose_name_plural = "Изображения постов"

    def __str__(self):
        return f'Image for post {self.post.title}'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Имя тега")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Comment(TimeStampModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Пост")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор")
    body = models.TextField(verbose_name="Содержимое")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
