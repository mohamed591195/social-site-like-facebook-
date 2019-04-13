from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list_url'),
    path('add_rm_like/', views.PostLikeView, name='like_post_url'),
    path('<int:id>/all_liking_users/', views.LikingUsers, name='liking_users')
]