
from rest_framework import serializers
from .models import Profile
from social.models import Follow,Post
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class ProfileSerializer(serializers.ModelSerializer):
    user =serializers.SerializerMethodField()
    id=serializers.SerializerMethodField()
    follower_count=serializers.SerializerMethodField()
    following_count=serializers.SerializerMethodField()
    post_count=serializers.SerializerMethodField()
    #mutual_friends=serializers.SerializerMethodField()
    class Meta :
        model =Profile
        fields=['id','user','follower_count','following_count','post_count','bio','verified','pic']
    def get_user(self,obj):
        return obj.user.username
    def get_id(self,obj):
        return  obj.user.id
    def get_follower_count(self,obj):
        user=obj.user.id
        follow=Follow.objects.filter(following=user).count() #following=user defines people who follow us
        
        return follow
    def get_following_count(self,obj):
        user=obj.user.id
        follow=Follow.objects.filter(follower=user).count() #follower=user defines people we are following
        return follow
    def get_post_count(self,obj):
        user=obj.user.id
        post_num=Post.objects.filter(user=user).count()
        return post_num
class SignupSerializers(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_text':'password'},write_only=True)
    class Meta:
        model =User
        fields=['username','email','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def save(self):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        password =self.validated_data['password']
        password2=self.validated_data['password2']
        if password!=password2:
            raise serializers.ValidationError({'password':'Password does not match'})
        error=[]
        try:
            get_user=self.validated_data['username']
            validate_password(password=password,user=get_user)
        except ValidationError as e :
            error.append(e)
        if error:
            raise serializers.ValidationError({'password':error})

        user.set_password(password)
        user.save()
class UpdateProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=('bio','name')
    def save(self):
        user=self.instance
        profile=Profile(
            user=user,
            bio=self.validated_data['bio'],
            name=self.validated_data['name']
        )
        profile.save()

