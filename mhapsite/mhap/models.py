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

class PostManager(models.Manager):
    def user_list(self, *args, **kwargs):
        user = kwargs.items()[0][1]
        print type(user)
        return super(PostManager, self).all().filter(user_id=user)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)
    email_confirmed = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("mhap:index", kwargs={"username": self.user})


class Post(models.Model):
     
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    secret = models.BooleanField(default=True)
    user_id = models.ForeignKey(Profile, null=True)
    objects = PostManager()

    
    
    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("mhap:detail", kwargs={"slug": self.slug})

    def get_list_url(self):
        return reverse("mhap:list")

    class Meta:
        ordering = ["-created", "-updated"]

# Create your models here.

@receiver(post_save, sender=User, dispatch_uid='update_user_profile')
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        print sender,instance,created
        Profile.objects.create(user=instance)
    instance.profile.save()


#https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html#sign-up-with-profile-model


def create_slug(instance, new_slug=None):
    slug = slugify(str(instance.title) + "-"+ str(instance.user_id.user))
    if new_slug is not None:
        slug = new_slug
    queryset = Post.objects.filter(slug=slug).order_by("-id")
    exists = queryset.exists()
    if exists:
        new_slug = "%s-%s" %(slug, queryset.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)