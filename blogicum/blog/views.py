from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView, ListView
)

from .models import Post, Category, Comment
from .forms import PostForm, UserEditForm, CommentForm
from .constants import PAGINATE_MAX_LENGHT


User = get_user_model()


class OnlyAuthorMixin(UserPassesTestMixin, SingleObjectMixin):
    """Миксин для проверки авторства"""

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        return redirect('blog:index')


class IndexView(ListView):
    """Представления для главной страницы"""

    model = Post
    paginate_by = PAGINATE_MAX_LENGHT
    template_name = 'blog/index.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        return Post.published.all().with_comment_count()


class CategoryView(LoginRequiredMixin, ListView):
    """Представления для отображения категории постов"""

    paginate_by = PAGINATE_MAX_LENGHT
    template_name = 'blog/category.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category.published,
                                          slug=self.kwargs['category_slug'])
        posts = self.category.posts(manager='published').all()
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostMixin:
    """Базовый миксин для всех моделей постов"""

    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostFormMixin:
    """Миксин для формы поста"""

    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(PostMixin, DetailView):
    """Представление для показа поста"""

    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        post: Post = super().get_object(queryset)
        if post.author == self.request.user:
            return post
        return super().get_object(Post.published.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context


class PostCreateView(PostMixin, PostFormMixin, LoginRequiredMixin, CreateView):
    """Представление для создания поста"""


class PostDeleteView(PostMixin, OnlyAuthorMixin, DeleteView):
    """Представление для удаления поста"""


class PostEditView(PostMixin, PostFormMixin, OnlyAuthorMixin, UpdateView):
    """Представление для изменения поста"""

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])


class CommentMixin:
    """Базовый миксин для комментария поста"""

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']})


class CommentFormMixin:
    """Миксин формаы комментария для поста"""

    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            Post,
            id=self.kwargs['post_id']
        )
        return super().form_valid(form)


class CommentCreateView(
    CommentMixin, CommentFormMixin, LoginRequiredMixin, CreateView
):
    """Представления для создания комментария к посту"""


class CommentDeleteView(
    CommentMixin, OnlyAuthorMixin, DeleteView
):
    """Представления для удаления комментария к посту"""


class CommentEditView(
    CommentMixin, CommentFormMixin, OnlyAuthorMixin, UpdateView
):
    """Представления для изменения комментария к посту"""


class ProfileView(ListView):
    """Представления для отображения профиля пользователя"""

    template_name = 'blog/profile.html'
    paginate_by = PAGINATE_MAX_LENGHT

    def get_queryset(self):
        self.profile = get_object_or_404(User,
                                         username=self.kwargs['username'])
        posts: Post = self.profile.posts.order_by('-pub_date')
        return posts.with_comment_count()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        return context

    def get_success_url(self):
        return reverse_lazy(
            'blog:index',
        )


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Представления для изменения профиля пользователя"""

    template_name = 'blog/user.html'
    form_class = UserEditForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )
