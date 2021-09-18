from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.response import Response
from .models import Follow, Post,Comment,Like
from rest_framework.decorators import api_view
from ipaddr import client_ip
from rest_framework.authentication import TokenAuthentication
from accounts.models import Profile
from .serializers import NewPostSerializers, PostSerializers,CommentSerializers,CommentViewSerializers
from accounts.serializers import ProfileSerializer
from django.contrib.auth.models import User
from rest_framework.pagination import LimitOffsetPagination
# Create your views here.
import hashlib
@api_view(['GET'])
def home_api(request):
    if request.method=='GET':
        paginnation_classes=LimitOffsetPagination()
        authentication_classes=[TokenAuthentication]
        get_user=request.user
        if get_user.is_anonymous:
            return Response({'error':'Token not provided.'})
        user_profile=Profile.objects.get(user=get_user)
        user_profile.ipaddress=client_ip(request)
        user_profile.save()
        feeds_for_user=Post.objects.filter(user__following__follower=get_user)
        feeds_for_user=feeds_for_user.order_by('date_posted').reverse()
        feeds_for_user=paginnation_classes.paginate_queryset(feeds_for_user,request)
        size_of_feed_query=len(feeds_for_user)
        paginnation_classes.max_limit=size_of_feed_query
        if size_of_feed_query==0:
            #suggest some users 
            response={}
            get_minimal_user_profile_data=Profile.objects.filter(blocked='False')
            #get_profile_asc =get_minimal_user_profile_data.order_by('joined').reverse()
            for i in get_minimal_user_profile_data:
                
                profile_serializer=ProfileSerializer(i)
                val=i.id
                response[val]=profile_serializer.data
            return Response({'notification':'Follow some users to get started','follow':response})
        feeds_after_serialization=PostSerializers(feeds_for_user,many=True,context={'request':request})
        return paginnation_classes.get_paginated_response({'feed':feeds_after_serialization.data})
        #return Response({'feed':feeds_after_serialization.data})

@api_view(['POST'])
def newpost(request):
    if request.method=='POST':
        authentication_classes=[TokenAuthentication]
        get_user=request.user
        if get_user.is_anonymous:
            return Response({'error':'Token not provided'})
        user_Data =User.objects.get(username=get_user)

        user =Post(user=user_Data)
        
        
        serializers =NewPostSerializers(user.user,data=request.data)
    
        if serializers.is_valid():
            serializers.save()
            return Response({'post': 'Successfully posted'})
        return Response(serializers.errors)

@api_view(['GET'])
def post_view_of_user(request,slug):
    authentication=[TokenAuthentication]
    user=request.user
    
    if slug.isdigit():
        return Response({'error':'Type error Id provided.'})
    elif slug.isalpha:
        try:
            get_username=User.objects.get(username=slug)
            get_username=get_username.id
        except ObjectDoesNotExist:
            return Response({'error':'User does not exits'})
        
    if user.is_anonymous:
        return Response({'error':'Token not provided'})

    get_posts=Post.objects.filter(user=get_username)
    serializers=PostSerializers(get_posts,many=True)
    if request.method=='GET':
        profile_url='/accounts/api/profile/{}'.format(slug)
        return Response({'posts':serializers.data,'profile-url':profile_url})

    return Response({'error':serializers.error})
@api_view(['GET'])
def follow_api(request,slug):
    authentication_classes =[TokenAuthentication]
    get_user=request.user
    if get_user.is_anonymous:
        return Response({'error':'Token not provided'})
    try:
        get_username=User.objects.get(username=slug)
        #also get the id 
        #get_user_id =Profile.objects.get(user=get_username)
    except ObjectDoesNotExist:
        return Response({'error':'Profile does not exits'})
    if str(get_user)==str(get_username):
        return Response({'error':'Follow not allowed'})
    obj,create=Follow.objects.get_or_create(following=get_username,follower=request.user)
    get_profile_data=Profile.objects.get(uuid_all=get_username.id)
    print(get_profile_data.id)
    serializers=ProfileSerializer(get_profile_data)
    return Response({'profile':serializers.data})
@api_view(['GET'])
def followers_api(request,slug):
    authentication_classes=[TokenAuthentication]
    get_user=request.user
    if get_user.is_anonymous:
        return Response({'error':'Token not provided'})
    try:
        user=User.objects.get(username=slug)
    except ObjectDoesNotExist:
        return Response({'error':'Profile not found'})
    get_followers_list=Follow.objects.filter(following=user.id)    
    response=[]
    for i in get_followers_list:
        user_id=User.objects.get(username=i)
        profile_data=Profile.objects.get(uuid_all=user_id.id)
        profile_after_serialization=ProfileSerializer(profile_data)
        response.append(profile_after_serialization.data)
        
    return Response({'followers':response})
@api_view(['GET'])
def like_api(request,slug):
    authentication_classes=[TokenAuthentication]
    get_user=request.user
    if get_user.is_anonymous:
        return Response({'error':'No Token provided.'})
    try:
        get_post=Post.objects.get(post_short_link=slug)
        print(get_post)
    except ObjectDoesNotExist:
        return Response({'error':'Post not found'})
    obj,created=Like.objects.get_or_create(post=get_post,user=get_user,liked=True)
    if obj:
        return Response({'liked':'Added to likes'})
    else:
        
        return Response({'error':'Something unexcepted happended Try again Later'})

@api_view(['POST'])
def comment_create_api(request,slug):
    authentication_classes=TokenAuthentication
    get_user=request.user
    if get_user.is_anonymous:
        return Response({'error':'No token provided'})
    serializers=CommentSerializers(data=request.data,context={'request':request,'slug':slug})
    if serializers.is_valid():
        serializers.save()
        return Response({'comment':'Comment post successfully'})
    else:
        return Response({'error':serializers.error})
@api_view(['GET'])
def comment_view_api(request,slug):
    authentication_class=[TokenAuthentication]
    get_user=request.user
    if get_user.is_anonymous:
        return Response({'error':'No Token provided'})
    try:
        get_post_short_link=Post.objects.get(post_short_link=slug)
        get_comment=Comment.objects.filter(post_id=get_post_short_link)
        response=[]
        for i in get_comment:
            serializer=CommentViewSerializers(i)
            response.append(serializer.data)
        return Response({'comments':response})
    except ObjectDoesNotExist:
        return Response({'error':'No Post found'})

@api_view(['DELETE'])
def unfollow_api(request,slug):
    authentication_classes=[TokenAuthentication]
    get_user=request.user
    if get_user.is_anonymous:
        return Response({'error':'No Token provided'})
    try:
        get_profile=User.objects.get(username=slug)
        
        get_follow=Follow.objects.get(following=get_profile,follower=get_user)
        get_follow.delete()
        return Response({'unfollowed':'unfollowed successfully'})
    except ObjectDoesNotExist:
        return Response({'error':'No profile found'})        