from django.contrib import admin
from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status', 'pinned_post', 'tags']
    list_filter = ['status', 'created', 'publish', 'author', 'pinned_post']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug':('title',)}
    fields = ('title', 'slug', 'author', 'body', 'status', 'publish', 'pinned_post', 'cover_photo', 'post_photo_one', 'authors_photo', 'post_photo_two', 'post_photo_three', 'blockquote', 'tags') 
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'update']
    search_fields = ['name', 'email', 'body'] 