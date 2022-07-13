from distutils.command.upload import upload
from django.db import models
from users.models import User
# Create your models here.
class Post(models.Model):
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


