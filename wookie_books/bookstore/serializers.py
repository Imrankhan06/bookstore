from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer is a Django REST framework serializer for the Book model.

    It is used to convert Book instances to JSON representations and vice versa.
    This serializer includes the following fields: 'id', 'title', 'description',
    'cover_image', and 'price'.

    Inherits from:
        serializers.ModelSerializer: A base class for model serializers in Django REST framework.

    Attributes:
        Meta (class): A nested class that provides metadata options for the serializer.
    """
    class Meta:
        """
       Meta is a nested class that defines metadata options for the BookSerializer.

       Attributes:
           model (Model): The Django model class that the serializer is associated with (Book).
           fields (tuple): A tuple of field names that should be included in the serialized representation.
       """
        model = Book
        fields = ('id', 'title', 'description', 'cover_image', 'price')
