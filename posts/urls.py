from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list_url'),
    path('add_rm_like/', views.PostLikeView, name='like_post_url'),
    path('<int:id>/all_liking_users/', views.LikingUsers, name='liking_users'),
    path('create/', views.WritePost.as_view(), name='create_post_url'),
    path('userposts/<int:id>/', views.UserPosts.as_view(), name='user_posts_url'),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='post_detail_url')
]