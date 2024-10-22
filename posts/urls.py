from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list_url'),
    path('add_rm_like/', views.PostLikeView, name='like_post_url'),
    path('<int:id>/all_liking_users/', views.LikingUsers, name='liking_users'),
    path('create/', views.WritePost.as_view(), name='create_post_url'),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='post_detail_url'),
    path('most_rated_posts/', views.MostRatedPosts, name='most_rated_posts_url')
]