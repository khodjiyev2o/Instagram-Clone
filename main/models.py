from asyncio.windows_events import NULL
from distutils.command.upload import upload
from this import d
from django.db import models
from users.models import User
import uuid
from django.db.models.signals import post_save, post_delete,pre_delete
# Create your models here.



class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='posts',blank = True, null = True)
    posted = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete = models.CASCADE)
    description = models.CharField(max_length=150,blank=False)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return str(f"This is a post by {self.owner} having {self.likes}     likes")

    def add_like(sender,instance,created,**kwargs):
        obj = instance
        post = instance.post
        if created:
            liked_post = Post.objects.get(id=post.id)
            liked_post.likes+=1
            liked_post.save()
            
            

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")
    

    def __str__(self):
        return self.count

    class Meta:
        unique_together = (
            ('user', 'post'),
        )
     
   


class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")

    def __str__(self):
        return str(f"{self.follower}  started following {self.following}")

    def follow_yourself(sender,instance,created,**kwargs):
        if created:
            Follow.objects.create(follower=instance,following=instance)
    class Meta:
        unique_together = (
            ('follower', 'following'),
        )    

   


class Stream(models.Model):
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="following_stream")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="followed_user")
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    date = models.DateTimeField()


    def __str__(self):
        return str(f"{self.following} created new post , it is being shown to {self.user}")
    
    def add_stream_by_follow(sender,instance,created,**kwargs):
        follow = instance
        follower = follow.follower
        following = follow.following
        posts = Post.objects.filter(owner=following)
        if created:
            for post in posts:
                Stream.objects.create(post=post,following=following,date=post.posted,user=follower)

    def delete_stream_by_follow(sender,instance,**kwargs):
        follow = instance
        follower = follow.follower
        following = follow.following
        posts = Post.objects.filter(owner=following)
        for post in posts:
                Stream.objects.filter(post=post,following=following,date=post.posted,user=follower).delete()

    def add_stream_by_post(sender,instance,created,**kwargs):
        post = instance
        user = post.owner
        followers = Follow.objects.filter(following=user)
        if created:
            for follower in followers:
                Stream.objects.create(post=post,following=user,date=post.posted,user=follower.follower)

    def delete_stream_by_post(sender,instance,**kwargs):
        post = instance
        user = post.owner
        followers = Follow.objects.filter(following=user)
        for follower in followers:
            Stream.objects.filter(post=post,following=user,date=post.posted,user=follower.follower).delete()
    
"""
    def update_stream(sender,instance,created,**kwargs):
        follow = instance
        follower = follow.follower
        following = follow.following
        posts = Post.objects.filter(owner=following)
        if not created:
            for post in posts:
                stream_object = Stream.objects.filter(post=post,following=following,date=post.posted,user=follower.follower)
                try:
                    stream_object.update()
                except Stream.DoesNotExist:
                     Stream.objects.create(post=post,following=following,date=post.posted,user=follower)"""

                
            


#POST SIGNALS
post_save.connect(Stream.add_stream_by_post,sender=Post)
post_delete.connect(Stream.delete_stream_by_post,sender=Post)
#post_save.connect(Stream.update_stream,sender=Follow)

#FOLLOW SIGNALS
post_save.connect(Stream.add_stream_by_follow,sender=Follow)
post_delete.connect(Stream.delete_stream_by_follow,sender=Follow)

#USER SIGNALS
post_save.connect(Follow.follow_yourself,sender=User)


#Like SIGNALS
post_save.connect(Post.add_like,sender=Likes)