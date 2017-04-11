"""
Module for admin.py importing libraries and registering what we want to be shwon in admin site
"""

from django.contrib import admin

# Register your models here.
from .models import Profile
from .models import Post
from .models import Quote,ChatMessages

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Quote)
admin.site.register(ChatMessages)
