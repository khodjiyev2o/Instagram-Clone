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
