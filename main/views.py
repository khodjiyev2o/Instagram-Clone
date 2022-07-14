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
