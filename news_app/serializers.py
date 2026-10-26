from django.contrib.auth.models import User
from rest_framework import serializers

from .models import News


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'email': {'required': True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class NewsSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = News
        fields = ['id', 'title', 'summary', 'content', 'author', 'author_name', 'date_created']
        read_only_fields = ['author', 'date_created']

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Это поле обязательно.')
        return value

    def validate_content(self, value):
        if len(value) < 50:
            raise serializers.ValidationError('Минимум 50 символов.')
        return value
