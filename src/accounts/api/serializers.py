from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField,
	EmailField,
	)


User = get_user_model()


class UserCreateSerializer(ModelSerializer):
	email = EmailField(label='Email Address')
	email2 = EmailField(label='Confirm Email')
	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'email',
			'email2'
		]

		extra_kwargs = {"password":{"write_only":True}}


	def create(self, validated_data):
		print validated_data
		username = validated_data['username']
		email = validated_data['email']
		password = validated_data['password']
		user_obj = User(
				username = username,
				email = email,
			)
		user_obj.set_password(password)
		user_obj.save()
		return validated_data


	def validate_email2(self, value):
		data = self.get_initial()
		email1 = data.get('email')
		email2 = value
		if email1 != email2:
			raise ValidationError("Emails must match.")
		return value
