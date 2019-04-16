from django.urls import path
from . import views

app_name = 'comments'
urlpatterns = [
    path('post_comment/', views.CommentView, name='post_comment_url')
]