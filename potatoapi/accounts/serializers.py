
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
    badges =serializers.SerializerMethodField()
    #mutual_friends=serializers.SerializerMethodField()
    follower,following,post_num=0,0,0
    badges_list =[
        'https://i.pinimg.com/170x/c6/1d/b5/c61db53bf914bcc3df879c09517ef6fb.jpg',
        'https://toppng.com/uploads/preview/yan-cat-practice-vector-by-cheesefaceman1-on-deviantart-nyan-cat-emoji-gif-11563236761nimgongmvn.png',
        'https://img.favpng.com/5/0/15/nyan-cat-computer-icons-desktop-wallpaper-png-favpng-KPZZ22ZH3FzTtbxD2s5UG1VhZ.jpg'
        ]
    class Meta :
        model =Profile
        fields=['id','user','follower_count','following_count','post_count','bio','verified','pic','badges']
    def get_user(self,obj):
        return obj.user.username
    def get_id(self,obj):
        return  obj.user.id
    def get_follower_count(self,obj):
        user=obj.user.id
        follower=Follow.objects.filter(following=user).count() #following=user defines people who follow us
        
        return follower
    def get_following_count(self,obj):
        user=obj.user.id
        following=Follow.objects.filter(follower=user).count() #follower=user defines people we are following
        return following
    def get_post_count(self,obj):
        user=obj.user.id
        post_num=Post.objects.filter(user=user).count()
        return post_num
    '''def get_mutual_friends(self,obj):
        get_user=obj.user.id
        get_request_user=self.context.get('request').user
        get_list=Follow.objects.filter(following=get_user)
        return get_list'''
    def get_badges(self,obj):
        badges_list_Response =[]

        if self.post_num>=10:
            badges_list_Response.append(self.badges_list[2])
        if self.follower<=3 :
            badges_list_Response.append(self.badges_list[1])
        if self.following<=3:
            badges_list_Response.append(self.badges_list[0])
        return badges_list_Response    
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
        get_profile_data =Profile.objects.get(user=user)
       
        for i in self.validated_data:
            if i=='bio':

                get_profile_data.bio=self.validated_data[i]
                get_profile_data.save()
            elif i=='name':
                get_profile_data.name=self.validated_data[i]
                get_profile_data.save()
            elif i=='pic':
                get_profile_data.pic=self.validated_data[i]
                get_profile_data.save()


            
        

