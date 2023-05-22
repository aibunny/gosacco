from django.conf.urls import patterns, include, url
from django.contrib import admin

from members import views
from shares.models import Shares

member_urls = patterns('',
                       # Examples:
                       # url(r'^$', 'members.views.home', name='home'),
                       url(r'^users/$', views.UserList.as_view()),
                       url(r'^members/$', views.MemberList.as_view()),
                       url(r'^members/(?P<pk>[0-9]+)/$', views.MemberDetail.as_view()),
                       url(r'^members/(?P<pk>[0-9]+)/shares$', Shares.views.ShareDetail.as_view()),
                       url(r'^groups/$', views.GroupList.as_view()),
                       url(r'^groups/(?P<pk>[0-9]+)/$', views.GroupDetail.as_view()),
                       url(r'^groups/(?P<pk>[0-9]+)/members$', views.GroupMember.as_view()),

                       #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       )


