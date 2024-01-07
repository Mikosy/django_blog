from django import forms
from .models import *


class EmailPostForm(forms.Form):
    pass
#     name = forms.CharField(max_length=24)
#     email = forms.EmailField()
#     to = forms.EmailField()
#     comments = forms.CharField(required=False, widgets=forms.Textarea)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'body')


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = '__all__'