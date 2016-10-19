from django.contrib.auth.models import User
from rest_framework import serializers

import models


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for comments
    """
    username = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='username',
        queryset=User.objects.all()
     )
    content_url = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='url',
        queryset=models.ContentURL.objects.all()
     )
    
    class Meta:
        model = models.Comment
        fields = ('id', 'username', 'comment', 'content_url', 'date_created')