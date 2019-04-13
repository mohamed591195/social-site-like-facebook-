from django.template import Library
from datetime import datetime
from ..models import Post
register  = Library()

@register.filter(name='same_date_time')
def same_date_time(dt1, dt2):
    dt1 = datetime.strftime(dt1, '%m/%d/%y %I:%M%p')
    dt2 = datetime.strftime(dt2, '%m/%d/%y %I:%M%p')
    if dt1 == dt2:
        return True
    return False

@register.filter(name='is_liked')
def post_is_liked(post, user):
    post = Post.objects.get(id=post.id)
    if post.user_likes.filter(id=user.profile.id).exists():
        return 'dislike'
    return 'like'