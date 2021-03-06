"""potatoapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
""" 
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from social.views import (
    newpost, post_view_of_user,home_api,follow_api,followers_api,
    like_api,comment_create_api,comment_view_api,unfollow_api,sticker_api,create_sticker_api,
    user_comment_list
    )
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('apinav/', include('rest_framework.urls')),
    path('newpost/',newpost,name='newpost'),
    path('user-posts/<str:slug>/',post_view_of_user,name='post-of-user'),
    path('api/home/',home_api,name='homeapi'),
    path('api/follow/<str:slug>/',follow_api,name='followapi'),
    path('api/followers/<str:slug>/',followers_api,name='followerslist'),
    path('api/like/<str:slug>/',like_api,name='likeapi'),
    path('api/comment/<str:slug>/',comment_create_api,name='commentapi'),
    path('api/comment/view/<str:slug>/',comment_view_api,name='commentviewapi'),
    path('api/unfollow/<str:slug>/',unfollow_api,name='unfollowapi'),
    path('api/stickers/',sticker_api,name='stickerapi'),
    path('api/stickers/create/',create_sticker_api,name='createstickerapi'),
    path('api/user/comments/<str:slug>/',user_comment_list,name='usercommentsapi')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
