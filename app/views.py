from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import decorators
from taggit.models import Tag
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
# forms
from .forms import *


def home(request, tag_slug=None):
    post_list = Post.published.all()
    pinned_post = Post.objects.filter(status=Post.Status.PUBLISHED)[:4]

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
        pinned_post = pinned_post.filter(tags__in=[tag])

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    subscribers_email = Newsletter.objects.all()

    if request.method == 'POST':
        form = NewsletterForm(request.POST)

        if form.is_valid():
            check_form = form.save(commit=False)
            if request.user.is_authenticated:
                check_form.user = request.user
            else:
                check_form.user = None

            check_form.save()
            messages.success(request, "You've subscribed successfully to our newsletter")


    else:
        form = NewsletterForm()

    args = {
        'posts': posts,
        'latest_post': pinned_post,
        'tag': tag,
        'subscribers_email': subscribers_email,
    }

    return render(request, 'app/index.html', args)


'''
Using class based views

'''

# class PostListView(ListView):

#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'app/index.html'

'''
Class based view end
'''


def post_detail(request, year, month, day, post):
    pinned_post = Post.objects.filter(status=Post.Status.PUBLISHED)[:4]

    posts = get_object_or_404(Post,
                              status=Post.Status.PUBLISHED,
                              slug=post,
                              publish__year=year,
                              publish__month=month,
                              publish__day=day)

    words = posts.body.split()
    word_count = len(words)

    # Calculating the reading time of my blog post
    average_reading_speed = 200
    reading_time_minutes = word_count / average_reading_speed
    reading_time_minutes = round(reading_time_minutes)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_form = form.save(commit=False)
            if request.user.is_authenticated:
                comment_form.user = request.user
            else:
                comment_form.user = None

                comment_form.save()
                print('form submitted successfully', comment_form)

    else:
        form = CommentForm()
        print('Error occured')

    comments = Comment.objects.filter(active=True)

    # creating function for getting similar posts using tags
    post_tags_ids = posts.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
        .exclude(id=posts.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]

    data = {
        'posts': posts,
        'form': form,
        'reading_time': reading_time_minutes,
        'comments': comments,
        'similar_posts': similar_posts,
        'latest_post': pinned_post,
    }

    return render(request, 'app/detail.html', data)


def search(request):
    pinned_post = Post.objects.filter(status=Post.Status.PUBLISHED)[:4]

    if request.method == 'POST':
        search_term = request.POST['search_term']
        posts = Post.published.filter(title__icontains=search_term)

        context = {
            "posts": posts,
            "search_term": search_term,
            'latest_post': pinned_post,
        }
        return render(request, 'app/search.html', context)

    else:
        return redirect('/')


def view_all_posts(request):
    url = request.META.get('HTTP_REFERER')
    pinned_post = Post.objects.filter(status=Post.Status.PUBLISHED)[:4]
    posts = Post.objects.all()

    data = {
        'posts': posts,
        'latest_post': pinned_post,
    }

    return render(request, 'app/all_posts.html', data)


def add_post(request):
    url = request.META.get('HTTP_REFERER')
    authors = Post.objects.filter(author=request.user)

    posts = Post.objects.all()

    if request.method == 'POST':

        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            check_form = form.save(commit=False)
            check_form.user = request.user
            check_form.save()
            messages.success(request, "You've added a post")
            return redirect('app:home')

    else:
        form = PostForm()

    data = {
        'posts': posts,
        'form': form,
        'authors': authors,
    }

    return render(request, 'app/add_post.html', data)


def edit_post(request, post_id):
    url = request.META.get('HTTP_REFERER')
    posts = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=posts)

        if form.is_valid():
            edited_post = form.save(commit=False)
            edited_post.user = request.user
            edited_post.save()
            messages.success(request, "You've edited a post")
            return redirect(url)
    else:
        form = PostForm(instance=posts)

    data = {
        'posts': posts,
        'form': form,
    }

    return render(request, 'app/edit_post.html', data)


def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, "You've deleted a post")

        return redirect('app:home')

    return render(request, 'app/delete_confirmation.html', {'post': post})


# def post_share(request, post_id):

#     post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)


#     if request.method == 'POST':

#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#         else:
#             form = EmailPostForm()
#         return render(request, 'app/post-share.html', {'post':post, 'form':form, })


def template_test(request):
    return render(request, 'app/template-test.html')
