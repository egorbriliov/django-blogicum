from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from .constants import CHAR_FIELD_MAX_LENGHT
from .managers import (PublishedPostManager, PublishedCategoryManager,
                       WithCommentCountManager)


User = get_user_model()


class Published(models.Model):
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть.'
    )

    class Meta:
        abstract = True


class CreatedAt(models.Model):
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True


class Category(Published):
    """Модель представляющая тематическую категорию"""

    title = models.CharField(
        'Заголовок',
        max_length=CHAR_FIELD_MAX_LENGHT)
    description = models.TextField('Описание')
    slug = models.SlugField('Идентификатор',
                            unique=True,
                            help_text=('Идентификатор страницы для URL; '
                                       'разрешены символы латиницы, цифры, '
                                       'дефис и подчёркивание.'))

    objects = models.Manager()
    published = PublishedCategoryManager()

    class Meta:  # type: ignore
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(models.Model):
    """Модель представляющая георграфическую метку"""

    name = models.CharField(
        'Название места',
        max_length=CHAR_FIELD_MAX_LENGHT
    )

    class Meta:  # type: ignore
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Comment(CreatedAt):
    text = models.TextField('Текст')
    post = models.ForeignKey(
        'Post',
        null=False,
        blank=False,
        related_name='comments',
        on_delete=models.CASCADE,
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Post(Published, CreatedAt):
    """Модель представляющая публикации"""

    title = models.CharField(
        'Заголовок',
        max_length=CHAR_FIELD_MAX_LENGHT)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата и время публикации',
                                    help_text=('Если установить дату и время '
                                               'в будущем — можно делать '
                                               'отложенные публикации.'))

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации',
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Местоположение',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='posts',
        verbose_name='Категория',
    )

    image = models.ImageField('Фото',
                              upload_to='post_images',
                              blank=True)

    objects = WithCommentCountManager()
    published = PublishedPostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

    class Meta:  # type: ignore
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)
