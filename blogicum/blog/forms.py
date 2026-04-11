from django import forms
from django.contrib.auth import get_user_model

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',
                   'is_published',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%d.%m.%Y %H:%M',
                attrs={'type': 'datetime-local'},
            ),
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['username'].help_text = None


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(
                attrs={'cols': '50', 'rows': '1'}
            )
        }
