from django.db import models
from django.utils import timezone
from account.models import Profile

class Post(models.Model):
    STATUS_CHOICES=(('published','P'), ('draft', 'D'))
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=25,)
    image = models.ImageField(verbose_name='upload image' ,upload_to='post/images', blank=True)
    content = models.TextField(blank=True)
    video = models.FileField(upload_to='post/videos', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title