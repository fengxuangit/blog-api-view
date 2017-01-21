from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField,
	)


from comments.api.serializers import (
	CommentCreateUpdateSerializer,
	)

from accounts.api.serializers import UserDetailSerializer

from comments.models import Comment

from posts.models import Post



class PostCreateUpdateSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
			# 'id',
			'title',
			# 'slug',
			'content',
			'publish',
		]

list_detail_url = HyperlinkedIdentityField(
	 	view_name = 'posts-api:detail',
	 	lookup_field = 'slug'
	 	)

class PostListSerializer(ModelSerializer):
	url = list_detail_url
	delete_url = HyperlinkedIdentityField(
	 	view_name = 'posts-api:delete',
	 	lookup_field = 'slug'
	 	)
	user = UserDetailSerializer(read_only=True)
	image = SerializerMethodField()
	html = SerializerMethodField()
	comments = SerializerMethodField()
	class Meta:
		model = Post
		fields = [
			'url',
			'user',
			'id',
			'title',
			'slug',
			'content',
			'html',
			'publish',
			'delete_url',
			'image',
			'comments'
		]

	def get_image(self, obj):
		try:
			image = obj.image.url
		except:
			image = None
		return image

	def get_html(self, obj):
		return obj.get_markdown()

	def get_comments(self, obj):
		content_tyoe = obj.get_content_type
		object_id = obj.id
		c_qs = Comment.objects.filter_by_instance(obj)
		comments = CommentCreateUpdateSerializer(c_qs, many=True).data
		return comments


class PostDetailSerializer(ModelSerializer):
	url = list_detail_url
	user = UserDetailSerializer(read_only=True)
	image = SerializerMethodField()
	class Meta:
		model = Post
		fields = [
			'url',
			'id',
			'user'
			'title',
			'slug',
			'content',
			'publish',
			'image',
		]


	def get_image(self, obj):
		try:
			image = obj.image.url
		except:
			image = None
		return image



