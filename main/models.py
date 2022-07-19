from django.db import models
from users.models import User
from django.db.models.signals import post_save, post_delete
# Create your models here.

   
class Comment(models.Model):
    commenter =  models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.CharField(max_length=150)
   

    def __str__(self):
        return self.text


  
class Post(models.Model):
    image = models.ImageField(upload_to='posts',blank = True, null = True)
    posted = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete = models.CASCADE)
    description = models.CharField(max_length=150,blank=False)
    likers = models.ManyToManyField(User,blank=True,related_name='likers')
    comments = models.ManyToManyField(Comment,blank=True)
    def __str__(self):
        return str(f"This is a post by {self.owner} having {self.likes}     likes")
    @property
    def likes(self):
        return self.likers.count()
        
            
 


    
   


class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")

    def __str__(self):
        return str(f"{self.follower}  started following {self.following}")

    def follow_yourself(sender,instance,created,**kwargs):
        admin = User.objects.get(id=1)
        if created:
            Follow.objects.create(follower=instance,following=instance)
            Follow.objects.create(follower=instance,following=admin)
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
