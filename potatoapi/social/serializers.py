import hashlib
from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from hashlib import blake2b
class NewPostSerializers(serializers.ModelSerializer):

    class Meta:
        model=Post
        fields=['post','pic']
    
    def save(self):
        user=self.instance #user data receiver 
        get_id_ =Post.objects.latest('id')
        
        shrt_url=blake2b(digest_size=get_id_.id).hexdigest()
        post=Post(
            user=user,
            post=self.validated_data['post'],
            pic=self.validated_data['pic'],
            post_short_link=shrt_url,

        )

        post.save()
#this is common for all post serialisations 
class PostSerializers(serializers.ModelSerializer):
    user=serializers.SerializerMethodField()
    id=serializers.SerializerMethodField()
    
    class Meta:
        model=Post
        fields=['id','user','date_posted','post','pic','video','like_count','comment_count','blocked']
    
    def get_user(self,obj):
        return obj.user.username
    def get_id(self,obj):
        return obj.post_short_link
    
    
