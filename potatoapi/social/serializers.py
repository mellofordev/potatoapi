
from rest_framework import serializers
from .models import Post,Like,Comment,Notification, Sticker
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
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
    user_profile_pic=serializers.SerializerMethodField()
    liked=serializers.SerializerMethodField()
    like_count=serializers.SerializerMethodField()
    comment_count=serializers.SerializerMethodField()
    verified=serializers.SerializerMethodField()
    #get_request_user= serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model=Post
        fields=['id','user','user_profile_pic','verified','date_posted','post','pic','video','like_count','comment_count','blocked','liked']

    def get_user(self,obj):
        return obj.user.username
    def get_id(self,obj):
        return obj.post_short_link
    def get_user_profile_pic(self,obj):
        data=str(obj.user.profile.pic)

        return '/media/{}'.format(data)
    def get_verified(self,obj):
        return obj.user.profile.verified
    def get_liked(self,obj):

        try:
            get_request_user=self.context.get("request").user
            Like.objects.get(post_id=obj,user=get_request_user)
            return True
        except ObjectDoesNotExist:
            return False
    def get_like_count(self,obj):
        try:
            get_user_like_details=Like.objects.filter(post_id=obj).count()
            return get_user_like_details
        except ObjectDoesNotExist:
            return 0
    def get_comment_count(self,obj):
        try:
            get_user_comment_count=Comment.objects.filter(post_id=obj).count()
            return get_user_comment_count
        except ObjectDoesNotExist:
            return 0
class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['comment']
    def save(self):
        get_user=self.context.get('request').user
        get_post_short_link=self.context.get('slug')
        get_post_id=Post.objects.get(post_short_link=get_post_short_link)
        comment=Comment(
            post=get_post_id,
            comment=self.validated_data['comment'],
            user=get_user

        )

        comment.save()

class CommentViewSerializers(serializers.ModelSerializer):

    user=serializers.SerializerMethodField()
    verified=serializers.SerializerMethodField()
    profile_pic=serializers.SerializerMethodField()

    class Meta:
        model=Comment
        fields=['user','verified','profile_pic','comment','sticker','sticker_id']

    def get_user(self,obj):

        return obj.user.username
    def get_verified(self,obj):
        return obj.user.profile.verified
    def get_profile_pic(self,obj):
        return str(obj.user.profile.pic)
class NotificationSerializers(serializers.ModelSerializer):
    fromuser=serializers.SerializerMethodField()
    touser=serializers.SerializerMethodField()
    class Meta:
        model=Notification
        fields=['fromuser','touser','_type','date','is_read']
    def get_fromuser(self,obj):
        print(obj)
        return obj.fromuser.username
    def get_touser(self,obj):
        return obj.touser.username
class StickerSerializers(serializers.ModelSerializer):
    class Meta:
        model=Sticker
        fields=['id','sticker_img_url','sticker_category','label']

class CreateStickerSerializers(serializers.ModelSerializer):
    class Meta:
        model=Sticker
        fields=['sticker_img_url','label','sticker_category']

        def save(self):
            
            sticker=Sticker(

                sticker_img_url=self.validated_data['sticker_img_url'],
                label=self.validated_data['label'],
                sticker_category=self.validated_data['sticker_category']
            )

            sticker.save()
