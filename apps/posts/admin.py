from django.contrib import admin


from .models import Post, PostImage, Comment, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    ...


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    ...


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ...


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    ...
