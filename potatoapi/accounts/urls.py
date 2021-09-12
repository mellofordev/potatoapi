from django.urls import path

from . import views as accounts_views
from rest_framework.authtoken import views
urlpatterns = [
    path('api/profile/all/',accounts_views.profile_view,name='profileapi'),
    path('api/profile/<str:slug>/',accounts_views.profile_username,name='profileid'),
    path('api/signup/',accounts_views.signup_view,name='signupapi'),
    path('api/login/',views.obtain_auth_token),
    path('profile/',accounts_views.user_profile,name='userprofile'),
    path('api/update/profile/',accounts_views.profile_update,name='updateprofile'),
    path('api/delete/',accounts_views.delete_user,name='deleteuser')
]