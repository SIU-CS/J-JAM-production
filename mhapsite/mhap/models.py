from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)



@receiver(post_save, sender=User, dispatch_uid='update_user_profile')
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        print sender,instance,created
        Profile.objects.create(user=instance)
    instance.profile.save()


#https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html#sign-up-with-profile-model

