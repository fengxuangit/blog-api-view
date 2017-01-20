from django.conf.urls import url
from django.contrib import admin

from .views import (
    UserCreateAPIView,
    )

urlpatterns = [
    url(r'^register$', UserCreateAPIView.as_view(), name='register'),
    # url(r'^create/$', CommentCreateAPIView.as_view(), name='create'),
    # url(r'^(?P<pk>\d+)/$', CommentDetailsAPIView.as_view(), name='detail'),
    # url(r'^(?P<id>\d+)/edit/$', CommentEditAPIView.as_view(), name='edit'),
    # url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
]
