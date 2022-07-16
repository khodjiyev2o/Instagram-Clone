from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import User
from main.models import Post

from .serializers import UserSerializer,PostSerializer

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from rest_framework import generics, authentication
# Create your views here.




@api_view(['GET'])
def usersapi(request):
    queryest = User.objects.all()
    serializer = UserSerializer(queryest,many=True)
    return Response(serializer.data)


class PostCreateApiView(generics.CreateAPIView):
    queryset =  Post.objects.all()
    serializer_class = PostSerializer


class PostApiView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailApiView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'


class PostUpdateApiView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        id = data['id']
        color = data['color']
        userid = data['user']

        post = Post.objects.get(id=id)

        user = User.objects.get(id=userid)

        

        if color == "red":
            post.likers.add(user)
            post.save()
        else:
            post.likers.remove(user.id)
            post.save()
        

        return Response("hi")

    