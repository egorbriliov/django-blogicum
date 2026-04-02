from django.db import models

from .querysets import PostQuerySet, CategoryQuerySet


class PublishedPostManager(models.Manager):
    def get_queryset(self) -> PostQuerySet:
        return (
            PostQuerySet(self.model)
            .published()
            .before_current_time()
        )


class PublishedCategoryManager(models.Manager):
    def get_queryset(self) -> CategoryQuerySet:
        return CategoryQuerySet(self.model).published()
