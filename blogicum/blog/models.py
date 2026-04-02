from django.db import models
from django.contrib.auth import get_user_model

from core.models import PublishedModel
from .constants import CHAR_FIELD_MAX_LENGHT
from .managers import PublishedCategoryManager, PublishedPostManager
from .querysets import CategoryQuerySet, PostQuerySet


User = get_user_model()


class Category(PublishedModel):
    """Модель представляющая тематическую категорию"""

    title = models.CharField('Заголовок', max_length=CHAR_FIELD_MAX_LENGHT)
    description = models.TextField('Описание')
    slug = models.SlugField('Идентификатор',
                            unique=True,
                            help_text=('Идентификатор страницы для URL; '
                                       'разрешены символы латиницы, цифры, '
                                       'дефис и подчёркивание.'))

    objects = CategoryQuerySet.as_manager()
    published: PublishedCategoryManager = PublishedCategoryManager()

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    """Модель представляющая георграфическую метку"""

    name = models.CharField('Название места', max_length=CHAR_FIELD_MAX_LENGHT)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishedModel):
    """Модель представляющая публикации"""

    title = models.CharField('Заголовок', max_length=CHAR_FIELD_MAX_LENGHT)
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

    objects = PostQuerySet.as_manager()
    published: PublishedPostManager = PublishedPostManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
