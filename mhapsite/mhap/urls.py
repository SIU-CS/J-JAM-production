"""
Contains mhap specific urls
first paramemter is the url,
second is the url in views
third is url name to easily reference in views
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list/$', views.post_list, name="list"),
    url(r'^create/$', views.post_create, name="create"),
    url(r'^list/(?P<slug>[\w-]+)/$', views.post_detail, name='detail'),
    url(r'^list/(?P<slug>[\w-]+)/edit/$', views.post_update, name='update'),
    url(r'^list/(?P<slug>[\w-]+)/delete/$', views.post_delete),
    url(r'^settings/$', views.settings),
    url(r'^settings/password/$', views.change_password, name='change_password'),
    url(r'^bot/$', views.bot_page, name='bot_page'),
]