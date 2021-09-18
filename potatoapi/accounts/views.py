
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer,SignupSerializers,UpdateProfileSerializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication
from ipaddr import client_ip
@api_view(['GET'])
def profile_view(request): #for internal use, permission admin/staff only
    if request.method =='GET':
        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile, many=True)
        return Response({'data':serializer.data})
    else:
        return Response({'error':'Bad request '})
@api_view(['GET'])
def profile_username(request,slug):#profile api with slug <username>
    authentication_classes=[TokenAuthentication]
    response = {}
    try:
        user = User.objects.get(username=slug)
        get_user = request.user
        pass_value_user=Profile.objects.get(user=user.id)
        print(user,get_user)
        if str(user)==str(get_user):
            print(get_user, user)
            #change the url  in production
            response['editprofile'] = 'http://localhost:8000/accounts/api/update/profile/'
        else:
            response['editprofile']='false'
        serializer = ProfileSerializer(pass_value_user)
        return Response({'profile': serializer.data, 'update': response})
    except ObjectDoesNotExist:
        return Response({'profile': 'Profile not found', 'update': response})

@api_view(['POST'])
def signup_view(request):
    if request.method=='POST':
        serializers=SignupSerializers(data=request.data)
        response={}
        if serializers.is_valid():
            serializers.save()
            response['status']='User registered successfully'
            get_user=User.objects.get(username=request.data.get('username'))
            get_user.profile.ipaddress=client_ip(request)
            get_user.profile.uuid_all=get_user.id
            get_user.save()
            token,obj=Token.objects.get_or_create(user=get_user)
            response['token']=str(token)
        else:
            response=serializers.errors
        return Response(response)
@api_view(['GET'])

def user_profile(request): # edit profile api 
    authentication_classes=[TokenAuthentication]

    response={}
    try:
        user=request.user
        if user.is_anonymous:
            return Response({'profile':'Token not provided'})
        get_user = Profile.objects.get(user=user)
        serializer = ProfileSerializer(get_user,many=True,context={'request':request})
        response['editprofile']='/api/update/profile/'
    except ObjectDoesNotExist:
        response['login-url']='/api/login/'


    return Response({'profile':serializer.data,'login':response})


@api_view(['PUT'])
@login_required(login_url='/accounts/api/login/')
def profile_update(request):
    authentication_classes=[TokenAuthentication]
    user=request.user
    #profile=Profile.objects.get(user=user)
    
    serializer=UpdateProfileSerializers(user,data=request.data)
    print(serializer)
    response={}
    if serializer.is_valid():
        serializer.save()
        response['data']='Profile updated'
        return Response(response)
    return Response(serializer.errors)
@api_view(['DELETE'])
def delete_user(request):
    authentication_classes=[TokenAuthentication]
    get_user=request.user
    try:
        user = User.objects.get(username=get_user)
    except ObjectDoesNotExist:
        return Response({'profile':'Profile not found'})
    if str(user)==str(get_user):
        user.delete()
        return Response({'profile':'Profile deleted successfully'})
    else:
        return Response({'profile':'Delete method not allowed'})




