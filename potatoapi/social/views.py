from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from .models import Follow, Post,Comment,Like,Notification, Sticker
from rest_framework.decorators import api_view
from ipaddr import client_ip
from rest_framework.authentication import TokenAuthentication
from accounts.models import Profile
from .serializers import CreateStickerSerializers, NewPostSerializers, PostSerializers,CommentSerializers,CommentViewSerializers,NotificationSerializers, StickerSerializers
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
        response=[]
        if size_of_feed_query==0:
            #suggest some users

            get_minimal_user_profile_data=Profile.objects.filter(blocked='False')
            #get_profile_asc =get_minimal_user_profile_data.order_by('joined').reverse()
            for i in get_minimal_user_profile_data:

                profile_serializer=ProfileSerializer(i)
                val=i.id
                response.append(profile_serializer.data)
            #return Response({'follow':response})
        feeds_after_serialization=PostSerializers(feeds_for_user,many=True,context={'request':request})
        return paginnation_classes.get_paginated_response({'feed':feeds_after_serialization.data,'follow':response})
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
    pagination=LimitOffsetPagination()
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
    get_posts=get_posts.order_by('date_posted').reverse()
    feeds=pagination.paginate_queryset(get_posts,request)
    size_of_feed=len(feeds)
    pagination.max_limit=size_of_feed

    serializers=PostSerializers(feeds,many=True,context={'request':request})
    return pagination.get_paginated_response({'feed':serializers.data})

    #return Response({'error':serializers.error})
@api_view(['GET'])
def post_of_request_user(request):
    authentication_classes=[TokenAuthentication]
    pagination=LimitOffsetPagination()
    get_user=request.user
    get_posts=Post.objects.filter(user=get_user.id)
    get_posts=get_posts.order_by('date_posted').reverse()
    feeds=pagination.paginate_queryset(get_posts,request)
    pagination.max_limit=len(feeds)
    serializer=PostSerializers(feeds,many=True,context={'request':request})
    return pagination.get_paginated_response({'feed':serializer.data})
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
    objs,created=Notification.objects.get_or_create(fromuser=get_user,touser=get_username,_type='Following',is_read=False)
    #get_profile_data=Profile.objects.get(uuid_all=get_username.id)

    #serializers=ProfileSerializer(get_profile_data)
    return Response({'follow':'Followed successfully'})
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
        profile_after_serialization=ProfileSerializer(profile_data,context={'request':request})
        response.append(profile_after_serialization.data)

    return Response({'followers':response})
@api_view(['GET'])
def following_api(request,slug):
    authentication_classes=[TokenAuthentication]
    get_user=request.user
    if get_user.is_anonymous:
        return Response({'error':'Token not provided'})
    try:
        user=User.objects.get(username=slug)
    except ObjectDoesNotExist:
        return Response({'error':'Profile not found'})
    get_followers_list=Profile.objects.filter(user__following__follower=user)
    response=[]
    for i in get_followers_list:
        user_id=User.objects.get(username=i)
        profile_data=Profile.objects.get(uuid_all=user_id.id)
        profile_after_serialization=ProfileSerializer(profile_data,context={'request':request})
        response.append(profile_after_serialization.data)

    return Response({'followers':response})
@api_view(['GET'])
def like_api(request,slug):
    authentication_classes=[TokenAuthentication]
    get_user=request.user
    get_post_id_=0
    if get_user.is_anonymous:
        return Response({'error':'No Token provided.'})
    try:
        get_post=Post.objects.get(post_short_link=slug)
        get_post_id_=get_post.id
    except ObjectDoesNotExist:
        return Response({'error':'Post not found'})
    obj,created=Like.objects.get_or_create(post=get_post,user=get_user,liked=True)

    if obj:
        objs,create=Notification.objects.get_or_create(fromuser=get_user,touser=get_post.user,_type='Liked',reference_id=get_post_id_,is_read=False)
        return Response({'liked':'Added to likes'})
    else:

        return Response({'error':'Something unexcepted happended Try again Later'})
@api_view(['DELETE'])
def unlike_api(request,slug):
    authentication_classes=[TokenAuthentication]
    get_user=request.user
    get_post_id_=0
    if get_user.is_anonymous:
        return Response({'error':'No Token provided.'})
    try:
        get_post=Post.objects.get(post_short_link=slug)
        get_post_id_=get_post.id
    except ObjectDoesNotExist:
        return Response({'error':'Post not found'})
    like_objs=Like.objects.get(post=get_post,user=get_user)
    get_Notification=Notification.objects.get(fromuser=get_user,touser=get_post.user,_type='Liked',reference_id=get_post_id_)
    if like_objs.liked==True:
        like_objs.delete()

        get_Notification.delete()
        return Response({'liked':'Deleted likes'})
    else:

        return Response({'error':'Something unexcepted happended Try again Later'})

@api_view(['POST'])
def comment_create_api(request,slug):
    authentication_classes=TokenAuthentication
    get_user=request.user
    if get_user.is_anonymous:
        return Response({'error':'No token provided'})
    serializers=CommentSerializers(data=request.data,context={'request':request,'slug':slug})
    get_post=Post.objects.get(post_short_link=slug)
    if serializers.is_valid():
        serializers.save()
        obj,create=Notification.objects.get_or_create(fromuser=get_user,touser=get_post.user,_type='Commented',reference_id=get_post.id)
        return Response({'comments':'Comment post successfully'})
    else:
        return Response({'error':serializers.data})
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
        return Response({'comment':response})
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
        get_Notification=Notification.objects.get(fromuser=get_user,touser=get_profile,_type='Following')
        get_Notification.delete()
        get_follow.delete()
        return Response({'unfollowed':'unfollowed successfully'})
    except ObjectDoesNotExist:
        return Response({'error':'No profile found'})
@api_view(['GET'])
def notification_view_api(request):
    authentication_class=[TokenAuthentication]
    get_user=request.user
    if get_user.is_anonymous:
        return Response({'error':'No token provided'})

    try:
        get_notification=Notification.objects.filter(touser=get_user.id)

    except ObjectDoesNotExist:
        return Response({'notification':'No notification'})
    if len(get_notification)!=0:
        for i in get_notification:
            i.is_read=True
            i.save()

    response=[]
    for i in get_notification:
        serializer=NotificationSerializers(i)
        response.append(serializer.data)
    return Response({'notification':response})

@api_view(['GET'])
def notification_count_api(request):
    authentication=[TokenAuthentication]
    get_user=request.user
    if get_user.is_anonymous:
        return Response({'error':'Token not provided'})
    try:
        notification_count=Notification.objects.filter(touser=get_user,is_read=False).count()
    except ObjectDoesNotExist:
        return Response({'notificationacount':0})
    return Response({'notificationcount':notification_count})
@api_view(['GET'])
def sticker_api(request):
    authentication_classes=TokenAuthentication
    if request.user.is_anonymous:
        return Response({'error':'Token not provided.'})
    
    try:
        get_stickers=Sticker.objects.all()
    except ObjectDoesNotExist:
        return Response({'error':'No stickers available.'})
    serializers_list=[]    
    for sticker_objs in get_stickers:
        serializers=StickerSerializers(sticker_objs)
        serializers_list.append(serializers.data)
    return Response({'stickers':serializers_list})

@api_view(['POST'])
def create_sticker_api(request):
    authentication_classes=TokenAuthentication
    if request.user.is_anonymous:
        return Response({'error':'Token not provided.'})
    
    serializer =CreateStickerSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'sticker':'Sticker created successfully'})
    else:
        return Response({'error':'Something went wrong'})
@api_view(['GET'])
def user_comment_list(request,slug):
    authentication_classes =[TokenAuthentication]
    if request.user.is_anonymous:
        return Response({'error':'Token not provided'})

    try:
        get_user=User.objects.get(username=slug)
        get_all_user_comment=Comment.objects.filter(user=get_user)
        comment_bucket=[]
        for i in get_all_user_comment:
            serializer=CommentViewSerializers(i)
            comment_bucket.append(serializer.data)
        return Response({'comment':comment_bucket})
    except ObjectDoesNotExist:
        return Response({'sticker':'No comments'})
