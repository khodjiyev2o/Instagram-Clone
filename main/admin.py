from django.contrib import admin
from .models import Post, Follow
# Register your models here.

admin.site.register(Follow)
admin.site.register(Post)