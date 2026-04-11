from django.db import models
from django.utils import timezone


class PublishedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class PublishedCategoryQuerySet(PublishedQuerySet):
    ...


class PublishedPostQuerySet(PublishedQuerySet):
    def before_current_time(self):
        return self.filter(pub_date__lt=timezone.now())

    def category_published(self):
        return self.filter(category__is_published=True)
