from django.db import models
from django.contrib.auth import get_user_model
import uuid 
from datetime import datetime


User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    cover = models.ImageField(upload_to='covers', default='default-cover.jpg')
    avatar = models.ImageField(upload_to='avatars', default='default-avatar.jpg')
    location = models.CharField(max_length=100,blank=True)
    relationship = models.CharField(max_length=100, blank=True)
    workingat = models.CharField(max_length=100,blank=True)
    follow_me = models.BooleanField(default=True)
    private_profile = models.BooleanField(default=False)
    show_online = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='posts')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now())
    likes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user


class likePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.username
    

class Follow(models.Model):
    user = models.CharField(max_length=100)
    following = models.CharField(max_length=100)


    def __str__(self) -> str:
        return self.user