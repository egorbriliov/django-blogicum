from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView, ListView
)

from .models import Post, Category, Comment
from .forms import PostForm, UserEditForm, CommentForm
from .constants import PAGINATE_MAX_LENGHT


User = get_user_model()

"""
Global mixins
"""


class OnlyAuthorMixin(UserPassesTestMixin, SingleObjectMixin):

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        return redirect('blog:index')


"""
Main
"""


class IndexView(ListView):
    model = Post
    paginate_by = PAGINATE_MAX_LENGHT
    template_name = 'blog/index.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        return Post.published.filter(category__in=Category.published.all())


"""
Category
"""


class CategoryView(LoginRequiredMixin, ListView):
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


"""
Posts
"""


class PostMixin:
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostFormMixin:
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/detail.html'

    def get_object(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        if post.author != self.request.user:
            return get_object_or_404(Post.published.all(), id=post_id)
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context


class PostCreateView(PostMixin, PostFormMixin, LoginRequiredMixin, CreateView):
    ...


class PostDeleteView(PostMixin, OnlyAuthorMixin, DeleteView):
    ...


class PostEditView(PostMixin, PostFormMixin, OnlyAuthorMixin, UpdateView):
    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])


"""
Post | Comments
"""


class CommentMixin:
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']})


class CommentFormMixin:
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
    ...


class CommentDeleteView(
    CommentMixin, OnlyAuthorMixin, DeleteView
):
    ...


class CommentEditView(
    CommentMixin, CommentFormMixin, OnlyAuthorMixin, UpdateView
):
    ...


"""
User
"""


class ProfileView(ListView):
    template_name = 'blog/profile.html'
    paginate_by = PAGINATE_MAX_LENGHT

    def get_queryset(self):
        self.profile = get_object_or_404(User,
                                         username=self.kwargs['username'])
        posts = self.profile.posts.order_by('-pub_date')
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        return context

    def get_success_url(self):
        return reverse_lazy(
            'blog:index',
        )


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/user.html'
    form_class = UserEditForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )
