from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField

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
	class Meta:
		model = Post
		fields = [
			'url',
			'user',
			'id',
			'title',
			'slug',
			'content',
			'publish',
			'delete_url',
		]


class PostDetailSerializer(ModelSerializer):
	url = list_detail_url
	class Meta:
		model = Post
		fields = [
			'url',
			'id',
			'title',
			'slug',
			'content',
			'publish',
		]