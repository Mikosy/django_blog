from django import template
from . .models import *

from django.db.models import Count

from django.utils.html import format_html

# using markdown
from django.utils.safestring import mark_safe
import markdown


register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('app/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

# this function tells which post have the heighest comments

@register.simple_tag
def get_most_commented_posts(count=2):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

# this function handles customized textfield

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.filter(name='truncate_words')
def truncate_words(value, arg):
    try:
        words = value.split()
        if len(words) > arg:
            return format_html('{}...', ' '.join(words[:arg]))
        return value
    except Exception as e:
        return value