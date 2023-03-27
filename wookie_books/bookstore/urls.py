from django.urls import path
from .views import (BookListCreateView, BookDetailView, ListCreateBooksView,
                    UpdateBookView, UnpublishedBookView, UnPublishedBookDetailsView)

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book_list_create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('my_books/', ListCreateBooksView.as_view(), name='my_book_detail'),
    path('my_books/<int:pk>/', ListCreateBooksView.as_view(), name='my_book_search'),
    path('my_books/update/<int:pk>/', UpdateBookView.as_view(), name='my_books_update'),
    path('my_books/unpublish/<int:pk>/', UnpublishedBookView.as_view(), name='unpublished'),
    path('my_books/list_unpublish/', UnPublishedBookDetailsView.as_view(), name='list_unpublished_books'),
]
