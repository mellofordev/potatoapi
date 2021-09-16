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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from social.views import newpost, post_view_of_user,home_api,follow_api,followers_api,like_api
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('apinav/', include('rest_framework.urls')),
    path('newpost/',newpost,name='newpost'),
    path('user-posts/<str:slug>/',post_view_of_user,name='post-of-user'),
    path('api/home/',home_api,name='homeapi'),
    path('api/follow/<str:slug>/',follow_api,name='followapi'),
    path('api/followers/<str:slug>/',followers_api,name='followerslist'),
    path('api/like/<str:slug>/',like_api,name='likeapi')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
