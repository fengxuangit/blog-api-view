from django.db.models import Q
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

from comments.models import Comment
from .serializers import (
	CommentCreateUpdateSerializer,
	CommentDetailSerializer
)


class CommentCreateAPIView(CreateAPIView):
	queryset = Comment.objects.all()
	permission_classes = [IsAuthenticated]

	def get_serializer_class(self):
		model_type = self.request.GET.get("type")
		slug = self.request.GET.get("slug")
		parent_id = self.request.GET.get("parent_id", None)
		return create_comment_seriallzer(
			model_type=model_type,
			slug=slug,
			parent_id=parent_id,
			user=self.request.user
			)


class CommentListAPIView(ListAPIView):
	serializer_class = CommentCreateUpdateSerializer
	queryset = Comment.objects.all()
	# filter_backends = [SearchFilter, OrderingFilter]
	filter_backends = [DjangoFilterBackend]
	filter_fields = ['content', 'user__first_name']
	# search_fields = ['title', 'content', 'user__first_name']
	pagination_class =  PostPageNumberPagination #PageNumberPagination

	def get_queryset(self, *args, **kwargs):
		# queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs);
		queryset_list = Comment.objects.all();
		query = self.request.GET.get('q')
		if query:
			queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query)|
				Q(user__last_name__icontains=query)
				).distinct()
		return queryset_list
	

class CommentDetailsAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
	serializer_class = CommentDetailSerializer
	queryset = Comment.objects.all()
	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
	# lookup_url_kwarg = 'abc'
	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destory(request, *args, **kwargs)

	


class CommentEditAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
	queryset = Comment.objects.filter(id__gte=0)
	serializer_class = CommentDetailSerializer
	lookup_url_kwarg = 'id'

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destory(request, *args, **kwargs)

# class PostDeleteAPIView(DestroyAPIView):
# 	serializer_class = PostDetailSerializer
# 	queryset = Post.objects.all()
# 	lookup_field = 'slug'
	# lookup_url_kwarg = 'abc'