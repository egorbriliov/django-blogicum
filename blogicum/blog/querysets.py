from django.db import models
from django.utils import timezone
from django.db.models import Count


class WithCommentCountQuerySet(models.QuerySet):
    def with_comment_count(self):
        return self.annotate(comment_count=Count('comments'))


class PublishedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class PublishedCategoryQuerySet(PublishedQuerySet):
    ...


class PublishedPostQuerySet(PublishedQuerySet, WithCommentCountQuerySet):
    def before_current_time(self):
        return self.filter(pub_date__lt=timezone.now())

    def category_published(self):
        return self.filter(category__is_published=True)

    def ordering_by_pub_date(self):
        return self.order_by('-pub_date')
