from django.shortcuts import render
from .models import Stream,Follow,Post
from users.models import User
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import PostForm
# Create your views here.
def main(request):
    user = request.user
    streams = Stream.objects.filter(user=user).select_related('post','following')
    friends = Follow.objects.filter(follower=user).order_by('following').select_related('following')
    ids = []
    for friend in friends:
        id = friend.following.id
        ids.append(id)
    suggestions = User.objects.all().exclude(id__in=ids)
    return render(request,'main/index.html',{'streams':streams,'friends':friends,'suggestions':suggestions})


class PostCreateView(CreateView):
    model = Post
    template_name = 'main/new_post.html'
    success_url = '/'
    form_class = PostForm
    
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(PostCreateView, self).form_valid(form)


def profile(request,pk):
    user = request.user
    posts_count = user.post_set.all().count()
    posts = Post.objects.filter(owner=user)
    follows_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    context = {
        'follows_count':follows_count,
        'following_count':following_count,
        'posts_count':posts_count,
        'posts':posts,
    }
    return render(request,'main/profile.html',{'context':context})