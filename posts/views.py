from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from common.decorators import is_ajax


class PostListView(ListView):
    template_name = 'posts/post_list.html'
    model = Post
    context_object_name = 'posts'


@login_required
@require_POST
@is_ajax
def PostLikeView(request):

    post_id = int(request.POST.get('id'))

    post = get_object_or_404(Post, id=post_id)
    action = ''
    if post.user_likes.filter(id=request.user.profile.id):
        post.user_likes.remove(request.user.profile)
        action = 'like'
    else:
        post.user_likes.add(request.user.profile)
        action='dislike'
    total_likes = post.user_likes.all().count()
    print(total_likes)
    return JsonResponse({'total_likes': total_likes, 'action': action})

def LikingUsers(request, id):
    post = Post.objects.get(id=id)
    users = post.user_likes.all()

    return render(request, 'posts/liking_users.html', {'users': users})