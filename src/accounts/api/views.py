from django.db.models import Q
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)

from rest_framework.mixins import (
	DestroyModelMixin,
	UpdateModelMixin,
	)

from rest_framework.generics import (
	ListAPIView,
	CreateAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	UpdateAPIView,
	DestroyAPIView
	)

from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination

from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
	)


from .serializers import (
	UserCreateSerializer,
)


User = get_user_model()

class UserCreateAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer
	queryset = User.objects.all()