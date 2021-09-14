
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
import datetime
User._meta.get_field('email')._unique = True

locker=(('on','ON'),('off','OFF'))
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    name= models.CharField(max_length=50,null=True, blank=True)
    uuid_all=models.IntegerField(null=True)
    pic=models.ImageField(default='default.png',upload_to='profilepic',null='True')
    verified=models.BooleanField(default=False)
    blocked=models.BooleanField(default=False)
    forcelock= models.CharField(max_length=3, choices=locker, default='off')
    ipaddress=models.GenericIPAddressField(null=True)
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

