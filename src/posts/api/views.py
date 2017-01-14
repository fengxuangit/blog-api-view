from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)

from rest_framework.generics import (
	ListAPIView,
	CreateAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	UpdateAPIView,
	DestroyAPIView
	)

from .permissions import IsOwnerOrReadOnly
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination

from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
	)

from posts.models import Post
from .serializers import (
	PostDetailSerializer,
	PostCreateUpdateSerializer,
	PostListSerializer
)


class PostCreateUpdateAPIView(CreateAPIView):
	serializer_class = PostCreateUpdateSerializer
	queryset = Post.objects.all()
	permission_classes = [IsOwnerOrReadOnly]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class PostListAPIView(ListAPIView):
	serializer_class = PostListSerializer
	queryset = Post.objects.all()
	# filter_backends = [SearchFilter, OrderingFilter]
	filter_backends = [DjangoFilterBackend]
	filter_fields = ['title', 'content']
	# search_fields = ['title', 'content', 'user__first_name']
	pagination_class =  PostPageNumberPagination #PageNumberPagination

	def get_queryset(self, *args, **kwargs):
		# queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs);
		queryset_list = Post.objects.all();
		query = self.request.GET.get('q')
		if query:
			queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query)|
				Q(user__last_name__icontains=query)
				).distinct()
		return queryset_list
	

class PostDetailsAPIView(RetrieveAPIView):
	serializer_class = PostDetailSerializer
	queryset = Post.objects.all()
	lookup_field = 'slug'
	# lookup_url_kwarg = 'abc'

class PostUpdateAPIView(RetrieveUpdateAPIView):
	serializer_class = PostCreateUpdateSerializer
	queryset = Post.objects.all()
	lookup_field = 'slug'

	def perform_update(self, serializer):
		serializer.save(user=self.request.user)
	# lookup_url_kwarg = 'abc'

class PostDeleteAPIView(DestroyAPIView):
	serializer_class = PostDetailSerializer
	queryset = Post.objects.all()
	lookup_field = 'slug'
	# lookup_url_kwarg = 'abc'