from django import forms
from taggit.forms import TagWidget
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body', 'comment_photo']


class PostForm(forms.ModelForm):
    tags = forms.CharField(widget=TagWidget(), required=False)
    class Meta:
        model = Post
        fields = ['title', 'slug', 'author', 'tags', 'authors_photo', 'cover_photo', 'body', 'blockquote', 'status', 'pinned_post', 'publish']


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']

# class SearchForm(forms.Form):
#     search_title = forms.CharField(label='Seach by title', max_length=100)
