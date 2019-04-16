from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment
from posts.models import Post
from .forms import CommentForm
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from action.models import Action

@login_required
@require_POST
def CommentView(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            if request.POST.get('post'):
                post_id = request.POST.get('post')
                post = get_object_or_404(Post, id=post_id)
                Comment.objects.create(profile=request.user.profile, comment=comment, target=post)
                Action.objects.create(profile=request.user.profile, verb='commented on', target=post)
                return redirect(reverse('posts:post_detail_url', kwargs={'slug': post.slug}))
            elif request.POST.get('_comment'):
                comment_id = request.POST.get('_comment')
                comment_obj = get_object_or_404(Comment, id=comment_id)
                Comment.objects.create(profile=request.user.profile, comment=comment, target=comment_obj)
                Action.objects.create(profile=request.user.profile, verb='replied on', target=comment_obj)
                post = comment_obj.post.all()[0]
                return redirect(reverse('posts:post_detail_url', kwargs={'slug': post.slug}))
    