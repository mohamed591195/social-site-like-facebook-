from django.db import models
from django.utils import timezone
from account.models import Profile
from django.urls import reverse

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100,)
    image = models.ImageField(verbose_name='upload image' ,upload_to='post/images', blank=True)
    content = models.TextField(blank=True)
    video = models.FileField(upload_to='post/videos', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user_likes = models.ManyToManyField(Profile, related_name='liked_posts', blank=True)
    updated = models.DateTimeField(auto_now=True)
    
    def get_liking_users(self):
        return reverse('posts:liking_users', args=[self.id])
        
    def __str__(self):
        return self.title