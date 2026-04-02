from django.db import models
from django.utils import timezone


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True, category__is_published=True)

    def before_current_time(self):
        return self.filter(pub_date__lt=timezone.now())


class CategoryQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)
