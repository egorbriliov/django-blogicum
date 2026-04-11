from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Location, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    @admin.display(description="Изображение")
    def post_photo(self, post: Post) -> str:
        if post.image:
            return mark_safe(f"<img src='{post.image.url}' width=50>")
        return "Без фото"

    @admin.display(description='Комментарии')
    def comment_count(self, post: Post):
        return f"{post.comments.count()}"

    list_display = (
        'post_photo',
        'pub_date',
        'title',
        'category',
        'author',
        'location',
        'comment_count',
    )
    readonly_fields = ['post_photo']
    list_editable = (
        'pub_date',
        'author',
        'location',
        'category'
    )
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'description',
    )
    list_editable = (
        'slug',
    )
    search_fields = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    search_fields = ('name',)
