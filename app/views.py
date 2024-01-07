from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.decorators.http import require_POST

from taggit.models import Tag


from .models import *

# forms
from .forms import *

# class based view 
from django.views.generic import ListView

# Create your views here.


def home(request, tag_slug=None):
    
    post_list = Post.published.all()
    pinned_post = Post.objects.filter(pinned_post=True)

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    return render(request, 'app/index.html', {'posts': posts, 'latest_post':pinned_post, 'tag':tag})



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
    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No post found")
    
    posts = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    # List of similar posts
    # post_tags_ids = post.tags.values_list('id', flat=True)
    # similar_posts = Post.published.filter(tags__in=post_tags_ids)\
    #     .exclude(id=post.id)
    # similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
    #     .order_by('-same_tags','-publish')[:4]
    
    # Count words in the post content
    words = posts.body.split()
    word_count = len(words)

    # Calculating the reading time of my blog post
    average_reading_speed = 200
    reading_time_minutes = word_count / average_reading_speed
    reading_time_minutes = round(reading_time_minutes)
    

    comments = Comment.objects.filter(active=True)

    form = CommentForm()
    

    data = {
        'posts':posts,
        'form': form,
        'reading_time':reading_time_minutes,
        'comments': comments,
        # 'similar_posts':similar_posts,
    }

    return render(request, 'app/detail.html', data)

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post,'form': form,'comment': comment})

# @require_POST
# def post_comment(request, post_id):
#     url = request.META.get('HTTP_REFERER')



#     post = get_object_or_404(Post, id=post_id,
#                              status=Post.Status.PUBLISHED)
#     comment = None

    
#     form = CommentForm(data=request.POST)

#     if form.is_valid():
#         comment_form = form.save(commit=False)
#         comment_form.post = post
#         comment_form.save()
#         # if comment_form.status_code == 200:
#         #     print("Email sent successfully!", comment_form.name, comment_form.body)
#         # else:
#         #     print("Failed to send email. Status code:", comment_form.status_code)

#         return redirect(url)
#     # else:
#     #     form = CommentForm()

#     return render(request, 'app/comment-form.html', {'form':form, 'post':post, 'comment': comment})



def search(request):

    
    if request.method == 'POST':
        search_term = request.POST['search_term']
        posts = Post.published.filter(title__icontains=search_term)

        context = {
            "posts": posts,
            "search_term": search_term,
        }
        return render(request, 'app/search.html', context)

    else:
        return redirect('/')


def view_all_posts(request):
    url = request.META.get('HTTP_REFERER')

    posts = Post.objects.all()

    if request.method == 'POST':

        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            check_form = form.save(commit=False)
            check_form.user = request.user
            check_form.save()
            return redirect(url)



    else:  
        form = PostForm()

    data = {
        'posts':posts,
        'form': form,
    }

    return render(request, 'app/all_posts.html', data)








def post_share(request, post_id):

    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)


    if request.method == 'POST':

        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
        else:
            form = EmailPostForm()
        return render(request, 'app/post-share.html', {'post':post, 'form':form, })
    




# @require_POST
# def post_comment(request, post_id):
#     post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
#     comment = None

#     form = CommentForm(data=request.POST)

#     if form.is_valid():

#         comment = form.save(commit=False)
#         comment.post = post
#         comment.save()

#     return render(request, '')