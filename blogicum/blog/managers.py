from django.db import models

from .querysets import (PublishedCategoryQuerySet, PublishedPostQuerySet,
                        WithCommentCountQuerySet)


class WithCommentCountManager(models.Manager):

    def get_queryset(self) -> WithCommentCountQuerySet:
        return WithCommentCountQuerySet(self.model)

    def with_comment_count(self):
        return self.get_queryset().with_comment_count()


class PublishedCategoryManager(models.Manager):
    def get_queryset(self) -> PublishedCategoryQuerySet:
        return (
            PublishedCategoryQuerySet(self.model)
            .published()
        )


class PublishedPostManager(WithCommentCountManager):
    def get_queryset(self) -> PublishedPostQuerySet:
        return (
            PublishedPostQuerySet(self.model)
            .before_current_time()
            .published()
            .category_published()
            .ordering_by_pub_date()
        )
