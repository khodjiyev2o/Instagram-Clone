from distutils.command.upload import upload
from django.db import models
from users.models import User
import uuid
from django.db.models.signals import post_save, post_delete
# Create your models here.


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='posts',blank = True, null = True)
    posted = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete = models.CASCADE)
    description = models.CharField(max_length=150,blank=False)

    def __str__(self):
        return str(self.description)


class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")

    def __str__(self):
        return str(f"{self.follower}  started following {self.following}")

class Stream(models.Model):
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="following_stream")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="followed_user")
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    date = models.DateTimeField()

    def add_stream(sender,instance,created,**kwargs):
        post = instance
        user = post.owner
        followers = Follow.objects.filter(following=user)
        if created:
            for follower in followers:
                Stream.objects.create(post=post,following=user,date=post.posted,user=follower.follower)

    def update_stream(sender,instance,created,**kwargs):
        post = instance
        user = post.owner
        followers = Follow.objects.filter(following=user)
        if not created:
            for follower in followers:
                Stream.objects.update(post=post,following=user,date=post.posted,user=follower.follower)

post_save.connect(Stream.add_stream,sender=Post)
post_save.connect(Stream.update_stream,sender=Post)