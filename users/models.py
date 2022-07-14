from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.translation import gettext_lazy as _
# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, username and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, 
        username and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user





class User(AbstractBaseUser):
  username = models.CharField(max_length = 50, unique = True)
  email = models.EmailField(_('email address'), unique = True)
  first_name = models.CharField(max_length = 5,blank = True, null = True)
  last_name = models.CharField(max_length = 5,blank = True, null = True)
  bio = models.CharField(max_length=200,blank = True, null = True)
  phone = models.CharField(max_length = 10,blank = True, null = True)
  image = models.ImageField(upload_to='user_ava',blank = True, null = True)
  is_admin = models.BooleanField(default=False)



  objects = MyUserManager()
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email', 'password']
  def __str__(self):
      return "{}".format(self.username)
  def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

  def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

  @property
  def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
