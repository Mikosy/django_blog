from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', _('Draft')
        PUBLISHED = 'PB', _('Published')

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    tags = TaggableManager()
    authors_photo = models.ImageField(upload_to='media', blank=True)
    cover_photo = models.ImageField(upload_to='media', blank=True)
    body = RichTextUploadingField(verbose_name=_("Body"))
    blockquote = models.TextField(max_length=200, blank=True, verbose_name=_("Blockquote"))
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    pinned_post = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name=_("Status"))

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name_plural = _("Posts")
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("app:post_detail", args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80, verbose_name=_("Name"))
    email = models.EmailField(verbose_name=_("Email"))
    body = models.TextField(verbose_name=_("Body"))
    comment_photo = models.ImageField(upload_to='media', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"


class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name=_("Email"))

    def __str__(self):
        return f'{self.email} subscribed to your newsletter'

    def clean(self):
        try:
            validate_email(self.email)
        except ValidationError as e:
            raise ValidationError({'Email': _("Invalid email format")})
