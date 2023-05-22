from django.conf.urls import patterns, include, url
from django.contrib import admin

import views


urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'members.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', views.ShareList.as_view()),
                       #url(r'^(?P<member_pk>[0-9]+)/$', views.SharesView.as_view()),
                       url(r'^sharepurchases/', views.SharePurchasesView.as_view()),
                       url(r'^sharetypes/$', views.ShareTypesView.as_view()),
                       url(r'^sharetransfers/$', views.ShareTransfersView.as_view()),
                       #url(r'^groups/(?P<pk>[0-9]+)/$', views.GroupDetail.as_view()),
                       #url(r'^groups/(?P<pk>[0-9]+)/members$', views.GroupMember.as_view()),
                       #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       )


