from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import User

from .serializers import UserSerializer

# Create your views here.




@api_view(['GET'])
def usersapi(request):
    queryest = User.objects.all()
    serializer = UserSerializer(queryest,many=True)
    return Response(serializer.data)