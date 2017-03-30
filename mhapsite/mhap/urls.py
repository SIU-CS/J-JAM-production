from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list/$', views.post_list, name="list"),
    url(r'^create/$', views.post_create),
    url(r'^list/(?P<slug>[\w-]+)/$', views.post_detail, name='detail'),
    url(r'^list/(?P<slug>[\w-]+)/edit/$', views.post_update, name='update'),
    url(r'^list/(?P<slug>[\w-]+)/delete/$', views.post_delete),
    url(r'^settings/$', views.settings),
]