from django.db import models
from django.utils import timezone
from account.models import Profile
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comment

class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100,)
    slug = models.SlugField(unique=True, db_index=True)
    image = models.ImageField(verbose_name='upload image' ,upload_to='post/images', blank=True)
    content = models.TextField(blank=True)
    video = models.FileField(upload_to='post/videos', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user_likes = models.ManyToManyField(Profile, related_name='liked_posts', blank=True)
    updated = models.DateTimeField(auto_now=True)
    comments = GenericRelation(Comment, content_type_field='target_ct', object_id_field='target_id', related_query_name='post')
    
    def get_liking_users(self):
        return reverse('posts:liking_users', args=[self.id])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:post_detail_url', kwargs={'slug': self.slug})
        
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']