from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone
# Create your models here.
class Post(models.Model):
    post=models.TextField(max_length=10000000,default='',null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    like_count=models.IntegerField(default=0)
    comment_count=models.IntegerField(default=0)
    date_posted=models.DateTimeField(default=timezone.now)
    pic = models.FileField(upload_to='postpics', null=True, blank=True)
    video = models.CharField(max_length=5, default='False')
    blocked=models.BooleanField(default=False)
    block_report=models.CharField(max_length=250,default='This post includes potentially sensitive content')
    post_short_link= models.SlugField(unique=True)

    def __str__(self):
        return str(self.pk)
    def get_id(self):
        return self.pk
class Comment(models.Model):
    post = models.ForeignKey('social.Post', on_delete=models.CASCADE,related_name='comment')
    comment=models.CharField(max_length=100,default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.comment
class Like(models.Model):
    post=models.ForeignKey('social.Post',on_delete=models.CASCADE,related_name='like')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    liked=models.BooleanField(default=False)
    def __str__(self):
        return str(self.user)


class Follow(models.Model):
    following=models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
    follower=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.follower.profile.name

