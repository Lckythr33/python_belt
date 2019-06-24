from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length = 60)
    last_name = models.CharField(max_length = 60)
    email = models.CharField(max_length = 60)
    password = models.CharField(max_length = 60)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    

class Quote(models.Model):
    quote = models.CharField(max_length = 60)
    author = models.CharField(max_length = 60)
    likecount = models.IntegerField(default=0)
    likedby = models.IntegerField(default=0)
    users = models.ManyToManyField(User, related_name="quotes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Like(models.Model):
    liked = models.BooleanField(default=False)
    quotes = models.ManyToManyField(Quote, related_name="likes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

