from django import forms
from .models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = '__all__'

class NewsletterForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ('email',)

# class SearchForm(forms.Form):
#     search_title = forms.CharField(label='Seach by title', max_length=100)