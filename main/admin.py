from django.contrib import admin
from .models import Post, Follow,Stream
# Register your models here.

admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(Stream)