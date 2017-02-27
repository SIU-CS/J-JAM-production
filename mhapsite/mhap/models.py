from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify

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

class Post(models.Model):
    # user_id = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    # slug = models.SlugField(unique=True)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    # secret = models.BooleanField()

    # objects = PostManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("mhap:detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-created", "-updated"]

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
