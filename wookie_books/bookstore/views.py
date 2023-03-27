from rest_framework import generics, permissions, filters
from rest_framework.response import Response

from .libs import constants
from .libs.validate_book import ValidateBook
from .models import Book
from .serializers import BookSerializer


class BookListCreateView(generics.ListAPIView):
    """
    Provides a list of published books and allows searching by title, description or author pseudonym.

    Parameters
    ----------
    search : str, optional
        Search query for filtering books by title, description or author pseudonym.

    Returns
    -------
    List of books : List[Book]
        Returns a list of published books matching the search query.
    """
    queryset = Book.objects.filter(published=True)
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'author__author_pseudonym', 'published']
    permission_classes = [permissions.AllowAny]


class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieves the details of a specific published book.

    Parameters
    ----------
    pk : int
        The primary key of the book to be retrieved.

    Returns
    -------
    Book
        Returns the details of the requested book.
    """
    queryset = Book.objects.filter(published=True)
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class ListCreateBooksView(generics.ListCreateAPIView):
    """
    Provides a list of published books authored by the authenticated user and allows creating new books.

    Parameters
    ----------
    search : str, optional
        Search query for filtering books by title, description or author pseudonym.

    Returns
    -------
    List of books : List[Book]
        Returns a list of published books authored by the authenticated user matching the search query.
    """
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'author__author_pseudonym']
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(author=self.request.user, published=True)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        title = self.request.POST['title']
        data = self.request.data
        code, status, j_path, j_schema = ValidateBook(user).validate(title, data)
        if code == "1006":
            return Response({
                'status_code': 422,
                'message': constants.CODE[code].format(j_path, j_schema)
            })

        if not status:
            return Response({
                'status_code': 200,
                'message': constants.CODE[code].format(user.username)
            })
        super().create(request, *args, **kwargs)
        return Response({
                'status_code': 201,
                'message': constants.CODE[code]
        })

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UpdateBookView(generics.UpdateAPIView):
    """
    Updates the details of a specific book authored by the authenticated user.

    Parameters
    ----------
    pk : int
        The primary key of the book to be updated.

    Returns
    -------
    Book
        Returns the updated details of the requested book.
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(author=self.request.user, published=True)


class UnPublishedBookDetailsView(generics.ListAPIView):
    """
    Provides a list of unpublished books authored by the authenticated user.

    Returns
    -------
    List of books : List[Book]
        Returns a list of unpublished books authored by the authenticated user.
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(author=self.request.user, published=False)


class UnpublishedBookView(generics.DestroyAPIView):
    """
    Unpublishes a specific book authored by the authenticated user.

    Parameters
    ----------
    pk : int
        The primary key of the book to be unpublished.

    Returns
    -------
    Response
        Returns a response with the status code and a message indicating the book has been unpublished.
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.unpublish()
        instance.save()
        return Response({
            'status_code': 200,
            'message': constants.CODE["1004"]
        })
