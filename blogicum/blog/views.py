from django.shortcuts import render, get_object_or_404
from .models import Post, Category

from .constants import POSTS_MAX_LENGHT


def index(request):
    post_list = (Post.
                 published.
                 all()
                 [:POSTS_MAX_LENGHT])
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post.published, pk=post_id)
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category.published, slug=category_slug)
    post_list = category.posts(manager='published').all()  # type: ignore
    context = {
        'post_list': post_list,
        'category': category
    }
    return render(request, 'blog/category.html', context)
