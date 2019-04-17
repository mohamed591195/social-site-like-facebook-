from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from .models import Post
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from common.decorators import is_ajax
from .forms import PostForm
from django.urls import reverse_lazy
from comments.forms import CommentForm
from action.models import Action
from django.db.models import Count


class PostListView(ListView):
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    extra_context = {
        'source': 'home'
    }
    def get_queryset(self):
        if self.request.user.is_authenticated:
            posts = []
            for user in self.request.user.following.all():
                posts += user.profile.posts.all()

            posts += self.request.user.profile.posts.all()
        else:
            posts = []
        return posts
    

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
        
        Action.objects.create(profile=request.user.profile, verb='liked', target=post)
    total_likes = post.user_likes.all().count()
    print(total_likes)
    return JsonResponse({'total_likes': total_likes, 'action': action})

def LikingUsers(request, id):
    post = Post.objects.get(id=id)
    users = post.user_likes.all()

    return render(request, 'posts/liking_users.html', {'users': users})

class WritePost(CreateView):
    form_class = PostForm
    template_name = 'posts/create.html'
    context_object_name = 'form'
    success_url = reverse_lazy('posts:post_list_url')
    extra_context = {
        'source': 'create_post'
    }
    def form_valid(self, form):
        new_form = form.save(commit=False)
        new_form.profile = self.request.user.profile
        self.object = new_form.save()
        Action.objects.create(profile=self.request.user.profile, verb='published new post', target=new_form)
        return super().form_valid(form)



class PostDetail(DetailView):
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    extra_context = {
        'form': CommentForm
    }
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Post.objects.filter(slug=slug)
    

def MostRatedPosts(request):
    # posts = Post.objects.annotate(num_likes=Count('user_likes')).order_by('-num_likes')
    posts = Post.objects.annotate(num_likes=Count('user_likes', distinct=True), num_comments=Count('comments', distinct=True)).order_by('-num_likes', '-num_comments')
    
    return render(request, 'posts/most_rated_posts.html', {'posts': posts, 'source': 'most_rated_posts'})