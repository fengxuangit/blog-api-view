from django.conf.urls import url
from django.contrib import admin

from .views import (
    CommentListAPIView,
    CommentDetailsAPIView,
    CommentCreateAPIView,
    CommentDetailsAPIView,
    CommentEditAPIView,
    )

urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name='list'),
    url(r'^create/$', CommentCreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', CommentDetailsAPIView.as_view(), name='detail'),
    url(r'^(?P<id>\d+)/edit/$', CommentEditAPIView.as_view(), name='edit'),
    # url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
]
