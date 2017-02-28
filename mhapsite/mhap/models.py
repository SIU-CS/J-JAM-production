from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# MVC MODEL VIEW CONTROLLER

# Post.objects.all()
# Post.objects.create(user=user, title="Some time")
# class PostManager(models.Manager):
#     def active(self, *args, **kwargs):
#         return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

# def upload_location(instance, filename):
#     return "%s/%s" %(instance.id, filename)
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, filename)



# def create_slug(instance, new_slug=None):
#     slug = slugify(instance.title)
#     if new_slug is not None:
#         slug = new_slug
#     queryset = Post.objects.filter(slug=slug).order_by("-id")
#     exists = queryset.exists()
#     if exists:
#         new_slug = "%s-%s" %(slug, queryset.first().id)
#         return create_slug(instance, new_slug=new_slug)
#     return slug

# def pre_save_post_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = create_slug(instance)

# pre_save.connect(pre_save_post_receiver, sender=Post)



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)
    email_confirmed = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User, dispatch_uid='update_user_profile')
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        print sender,instance,created
        Profile.objects.create(user=instance)
    instance.profile.save()


#https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html#sign-up-with-profile-model


class Post(models.Model):
    user_id = models.ForeignKey(Profile, default=-1)
    title = models.CharField(max_length=120)
    #slug = models.SlugField(unique=True,default='NULL')
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    secret = models.BooleanField(default=True)

    # objects = PostManager()

    

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("mhap:detail", kwargs={"id": str(self.user_id)})

    class Meta:
        ordering = ["-created", "-updated"]