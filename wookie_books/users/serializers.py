from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """A serializer for the CustomUser model. It serializes the 'username' and 'author_pseudonym' fields
        for API responses and handles deserialization for creating and updating CustomUser instances.
    """

    class Meta:
        model = CustomUser
        fields = ('username', 'author_pseudonym')
