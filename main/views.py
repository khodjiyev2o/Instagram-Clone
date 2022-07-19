from select import select
from urllib import request
from django.shortcuts import render
from django.urls import reverse
from .models import Stream,Follow,Post
from users.models import User
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import PostForm,ProfileForm 
from users.forms import RegistrationForm

# Create your views here.
def main(request):
    if request.user.is_authenticated:
        user = request.user
        streams = Stream.objects.select_related('post','following').filter(user=user).prefetch_related('post__likers','post__comments').order_by('-date')
        friends = Follow.objects.filter(follower=user).order_by('following').select_related('following')
        ids = []
        for friend in friends:
            id = friend.following.id
            ids.append(id)
        suggestions = User.objects.all().exclude(id__in=ids)
        return render(request,'main/index.html',{'streams':streams,'friends':friends,'suggestions':suggestions})

    else:
        forms = RegistrationForm()
        user = User.objects.get(id=1)
        streams = Stream.objects.select_related('post','following').filter(user=user).prefetch_related('post__likers','post__comments').order_by('-date')
        friends = Follow.objects.filter(follower=user).order_by('following').select_related('following')
        suggestions = User.objects.all()
        return render(request,'main/index.html',{'streams':streams,'suggestions':suggestions,'friends':friends,'forms':forms})
   
class PostCreateView(CreateView):
    model = Post
    template_name = 'main/new_post.html'
    success_url = '/'
    form_class = PostForm
    
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(PostCreateView, self).form_valid(form)

def no_user_new_post(request):
    return render(request,'main/no_user_new_post.html',{})


def profile(request,pk):
    user = User.objects.get(id=pk)
    posts = Post.objects.filter(owner=user)
    posts_count = user.post_set.all().count()
    posts = Post.objects.filter(owner=user)
    follows_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
   
    context = {
        'posts_count':posts_count,
        'following_count':following_count,
        'follows_count':follows_count,
        'user':user,
        'posts':posts,
    }
    return render(request,'main/profile.html',{'context':context})



def no_user_profile(request):
    return render(request,'main/no_user_profile.html',{})



class ProfileUpdateView(UpdateView):  
    model = User
    template_name = 'main/edit_profile.html'
   
    
    
   
     

    form_class = ProfileForm
    def get_success_url(self, **kwargs):
    # obj = form.instance or self.object
        return reverse("profile", kwargs={'pk': self.object.id})
    
    

   