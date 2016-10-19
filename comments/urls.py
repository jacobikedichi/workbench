import views

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^comments/$', views.CommentList.as_view()),
    #handles comment lookup by ids (i.e. /comments/3/)
    url(r'^comments/(?P<pk>[0-9]+)/$', views.CommentDetail.as_view()),
    #handles comment(s) lookup by content_url (i.e. /comments/low-altitude-launch/)
    url(r'^comments/(?P<content_url>[-\w]+)/$', views.CommentList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)