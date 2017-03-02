from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/$', views.index, name='index'),
    url(r'^(?P<username>[\w.@+-]+)/list/$', views.post_list, name="list"),
    url(r'^(?P<username>[\w.@+-]+)/list/create/$', views.post_create),
    url(r'^(?P<username>[\w.@+-]+)/list/(?P<slug>[\w-]+)/$', views.post_detail, name='detail'),
    url(r'^(?P<username>[\w.@+-]+)/list/(?P<slug>[\w-]+)/edit/$', views.post_update, name='update'),
    url(r'^(?P<username>[\w.@+-]+)/list/(?P<slug>[\w-]+)/delete/$', views.post_delete),
]