from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField,
	)

from comments.models import Comment

User = get_user_model()

def create_comment_serializer(mode_type='post', slug=None, parent_id=None):
	class CommentCreateSerializer(ModelSerializer):
		class Meta:
			model = Comment
			fields = [
				'id',
				'parent',
				'content',
				'timestamp',
			]

		def __init__(self, *args, **kwargs):
			self.mode_type = mode_type
			self.slug = slug
			self.parent_id = None
			if self.parent_id:
				parent_qs = Comment.objects.filter(id=parent_id)
				if parent_qs.exists() and parent_qs.count() == 1:
					self.parent_obj = parent_qs.first()
			return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

		def validate(self, data):
			mode_type = self.mode_type
			model_qs  = ContentType.objects.filter(model=mode_type)
			if not model_qs.exists() or model_qs.count() != 1:
				raise ValidationError("This is not valid content type")
			SomeModel = model_qs.first().model_class()
			obj_qs = SomeModel.objects.filter(slug=self.slug)
			if not obj_qs.exists() or obj_qs.count() != 1:
				raise ValidationError("This is not a slug for this content type")
			return data

		def create(self, validated_data):
			content = validated_data.get("content")
			if user:
				main_user = user
			else:
				user = User.objects.all().first()
				model_type = self.model_type
				slug = self.slug
				parent_obj = self.parent_obj
				comment = Comment.objects.create_by_model_type(
					model_type, slug, content, user, parent_obj=parent_obj)
			return Comment

	return CommentCreateSerializer

class CommentCreateUpdateSerializer(ModelSerializer):
	replies_count = SerializerMethodField()
	class Meta:
		model = Comment
		fields = [
			'id',
			'content_type',
			'object_id',
			'parent',
			'content',
			'replies_count',
		]

	def get_replies_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0



class CommentChildSerializer(ModelSerializer):
	class Meta:
		model = Comment
		fields = [
			'id',
			'content',
			'timestamp',
		]


class CommentDetailSerializer(ModelSerializer):
	replies = SerializerMethodField()
	reply_count = SerializerMethodField()
	class Meta:
		model = Comment
		fields = [
			'id',
			'content_type',
			'object_id',
			'content',
			'reply_count',
			'replies',
			'timestamp',
		]

		read_only_fields = [
			'content_type',
			'object_id',
			'reply_count',
			'replies',
		]
		

	def get_replies(self, obj):
		if obj.is_parent:
			return CommentChildSerializer(obj.children(), many=True).data
		return None

	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0

class CommentEditSerializer(ModelSerializer):
	class Meta:
		model = Comment
		fields = [
			'id',
			'content',
			'timestamp',
		]

	def get_replies(self, obj):
		if obj.is_parent:
			return CommentChildSerializer(obj.children(), many=True).data
		return None

	def get_replies_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0