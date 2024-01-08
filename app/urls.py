from django.urls import path
from app import views

from app.feeds import LatestPostsFeed


app_name = 'app'


urlpatterns = [
    path('', views.home, name='home'),
    path('tag/<slug:tag_slug>/', views.home, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='post_list'), 
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('search', views.search, name="search"),
    path('view_all_posts', views.view_all_posts, name='view_all_posts'),
    path('<int:post_id>/comment/', views.post_comment, name="post_comment"),
    path('feed/', LatestPostsFeed(), name='post_feed'),
]

