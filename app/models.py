from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User

from taggit.managers import TaggableManager

from django.urls import reverse

# Create your models here.

class PublishedManager(models.Manager):
    '''
    by default django retrieves data from the database by using the .objects manager. we can customize ours to retrieve data from the db using a custom manager
    '''
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    # Adding a status field that helps keep posts as draft until ready for publication
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'


    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

    tags = TaggableManager()

    authors_photo = models.ImageField(upload_to='media', height_field=None, width_field=None, max_length=None, blank=True)


    cover_photo = models.ImageField(upload_to='media', height_field=None, width_field=None, max_length=None, blank=True)
    post_photo_one = models.ImageField(upload_to='media', height_field=None, width_field=None, max_length=None, blank=True)
    post_photo_two = models.ImageField(upload_to='media', height_field=None, width_field=None, max_length=None, blank=True)
    post_photo_three = models.ImageField(upload_to='media', height_field=None, width_field=None, max_length=None, blank=True)

    body = models.TextField()
    blockquote = models.TextField(max_length=200, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    pinned_post = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    

    objects = models.Manager() #django manager
    published = PublishedManager() #custom manager



    class Meta:
        # Pluarlizes the name in the admin panel
        verbose_name_plural = 'Post'

        # It sorts datas by publish (a reversed order)
        ordering = ['-publish']

        # database indexes(it will improve performance for queries filtering)
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title
    
    # Use this when you want to use canonical url
    def get_absolute_url(self):
        return reverse("app:post_detail", args=[self.publish.year,
                                                self.publish.month,
                                                self.publish.day,
                                                self.slug])
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()

    comment_photo = models.ImageField(upload_to='media', height_field=None, width_field=None, max_length=None, blank=True)


    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post}"