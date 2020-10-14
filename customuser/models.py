from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    posts = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    givenName = models.CharField(max_length=150)
    familyName = models.CharField(max_length=150)
    REQUIRED_FIELDS = ['username', "password"]
    USERNAME_FIELD = "email"
    is_anonymous = False
    is_authenticated = True
    objects = UserManager()

    def __str__(self):
        return self.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_text = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.post_text


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

