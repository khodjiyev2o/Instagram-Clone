from django.shortcuts import render
from .models import Stream,Follow
from users.models import User
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