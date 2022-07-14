from django.contrib import admin
from .models import Post, Follow,Stream,Likes
# Register your models here.

admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(Stream)
admin.site.register(Likes)