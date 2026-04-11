from django.db import models

from .querysets import PublishedCategoryQuerySet, PublishedPostQuerySet


class PublishedCategoryManager(models.Manager):
    def get_queryset(self) -> PublishedCategoryQuerySet:
        return (
            PublishedCategoryQuerySet(self.model)
            .published()
        )


class PublishedPostManager(models.Manager):
    def get_queryset(self) -> PublishedPostQuerySet:
        return (
            PublishedPostQuerySet(self.model)
            .before_current_time()
            .published()
            .category_published()
        )
