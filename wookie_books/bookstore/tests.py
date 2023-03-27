from decimal import Decimal
from io import BytesIO

import jsonschema
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.test import APIRequestFactory

from .libs import constants
from .models import CustomUser, Book
from .serializers import BookSerializer

mock_book_schema = constants.BOOK_SCHEMA

mock_create_book = {
    "title": "Test Book",
    "description": "This is a test book.",
    "cover_image": SimpleUploadedFile("test_cover.jpg", b"file_content", content_type="image/jpeg"),
    "price": "9.99",
    "published": True
}

mock_create_user = {
    "username": "testuser",
    "password": "testpassword",
    "author_pseudonym": "testauthor"
}


# model
class BookTestCase(TestCase):
    """
    BookTestCase contains test cases for the Book model.

    Test cases:
        - test_book_created: Verifies that a book is created successfully with the correct attributes.
        - test_book_str_representation: Tests the string representation of a book using its title.
        - test_book_unpublish: Ensures the unpublish method sets the 'published' attribute to False.
        - test_unique_together_constraint: Checks that the unique_together constraint is enforced
                                           for the combination of 'title' and 'author' fields.

    The setUp method creates a CustomUser and a Book instance to be used in the test cases.
    """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username=mock_create_user.get("username"),
            password=mock_create_user.get("password"),
            author_pseudonym=mock_create_user.get("author_pseudonym")
        )

        self.book = Book.objects.create(
            title=mock_create_book.get("title"),
            description=mock_create_book.get("description"),
            author=self.user,
            cover_image=mock_create_book.get("cover_image"),
            price=mock_create_book.get("price"),
            published=mock_create_book.get("published")
        )

    def test_book_created(self):
        """Test that the book is created successfully."""
        self.assertEqual(self.book.title, mock_create_book.get("title"))
        self.assertEqual(self.book.description, "This is a test book.")
        self.assertEqual(self.book.author, self.user)
        self.assertIsNotNone(self.book.cover_image)
        self.assertEqual(str(self.book.price), "9.99")
        self.assertTrue(self.book.published)

    def test_book_str_representation(self):
        """Test the string representation of the book."""
        self.assertEqual(str(self.book), mock_create_book.get("title"))

    def test_book_unpublish(self):
        """Test that the unpublish method sets the published attribute to False."""
        self.book.unpublish()
        self.assertFalse(self.book.published)

    def test_unique_together_constraint(self):
        """Test that the unique_together constraint is enforced for title and author."""
        with self.assertRaises(Exception):
            Book.objects.create(
                title=mock_create_book.get("title"),
                description="This is another test book.",
                author=self.user,
                price="12.99",
                published=mock_create_book.get("published")
            )


class BookSerializerTestCase(TestCase):
    """
    Test cases for the BookSerializer class.

    Methods
    -------
    setUp():
        Sets up the test environment by creating a user and a book instance.

    test_book_serializer_serialization():
        Tests the serialization of a Book model instance using the BookSerializer.

    test_book_serializer_deserialization():
        Tests the deserialization of data using the BookSerializer to create a Book model instance.

    Returns
    -------
    None
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = CustomUser.objects.create_user(
            username=mock_create_user.get("username"),
            password=mock_create_user.get("password"),
            author_pseudonym=mock_create_user.get("author_pseudonym")
        )

        self.book = Book.objects.create(
            title=mock_create_book.get("title"),
            description=mock_create_book.get("description"),
            author=self.user,
            cover_image=mock_create_book.get("cover_image"),
            price=mock_create_book.get("price"),
            published=mock_create_book.get("published")
        )

        self.serializer = BookSerializer(instance=self.book)

    def test_book_serializer_data(self):
        """Test the serialized data from the BookSerializer."""
        expected_data = {
            'id': self.book.id,
            'title': mock_create_book.get("title"),
            'description': mock_create_book.get("description"),
            'cover_image': self.book.cover_image.url,
            'price': mock_create_book.get("price"),
        }
        self.assertDictEqual(self.serializer.data, expected_data)

    def test_book_serializer_deserialization(self):
        """Test deserialization of data with the BookSerializer."""
        image = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        data = {
            'title': 'New Test Book',
            'description': 'This is a new test book.',
            'cover_image': SimpleUploadedFile("new_test_cover.jpg", img_byte_arr, content_type="image/jpeg"),
            'price': '12.99',
            'author': self.user.id
        }
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        new_book = serializer.save(author=self.user)
        self.assertEqual(new_book.title, data['title'])
        self.assertEqual(new_book.description, data['description'])
        self.assertEqual(new_book.price, Decimal(data['price']))


class BookListCreateViewTestCase(APITestCase):
    """
    BookListCreateViewTestCase is a test case class for testing the BookListCreateView API view.
    The purpose of this test case is to ensure that the view works as expected, and the following
    functionality is tested:

    Retrieving a list of all published books.
    Proper filtering when searching for books based on title, description, or author's pseudonym.
    Ensuring that permissions are set correctly, allowing any user (authenticated or unauthenticated)
    to access the view.

    Parameters
    unittest.TestCase : A base test case class from the unittest module, which provides methods for
    assertions and test setup.

    Returns
    None
    """

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username=mock_create_user.get("username"),
            password=mock_create_user.get("password"),
            author_pseudonym=mock_create_user.get("author_pseudonym")
        )
        self.book = Book.objects.create(
            title=mock_create_book.get("title"),
            description=mock_create_book.get("description"),
            author=self.user,
            price=9.99
        )
        self.url = reverse('book_list_create')

    def test_list_books(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        response = self.client.get(self.url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class BookDetailViewTestCase(APITestCase):
    """
    BookDetailViewTestCase is a test case class for testing the BookDetailView API view.
    The purpose of this test case is to ensure that the view works as expected, and the
    following functionality is tested:

    Retrieving the details of a specific published book.
    Ensuring that only published books are accessible.
    Ensuring that permissions are set correctly, allowing any user
    (authenticated or unauthenticated) to access the view.

    Parameters
    unittest.TestCase : A base test case class from the unittest module, which provides
    methods for assertions and test setup.

    Returns
    None
    """

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username=mock_create_user.get("username"),
            password=mock_create_user.get("password"),
            author_pseudonym=mock_create_user.get("author_pseudonym")
        )
        self.book = Book.objects.create(
            title=mock_create_book.get("title"),
            description=mock_create_book.get("description"),
            author=self.user,
            price=9.99
        )
        self.url = reverse('book_detail', kwargs={'pk': self.book.pk})

    def test_get_book_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)


class ListCreateBooksViewTestCase(APITestCase):
    """
    ListCreateBooksViewTestCase is a test case class for testing the ListCreateBooksView API view.
    The purpose of this test case is to ensure that the view works as expected, and the following
    functionality is tested:

    Listing all published books for the authenticated user.
    Creating a new book for the authenticated user.
    Ensuring that the search functionality works correctly for title, description, and author pseudonym.
    Ensuring that permissions are set correctly, allowing only authenticated users to access the view.

    Parameters
    unittest.TestCase : A base test case class from the unittest module, which provides methods for
    assertions and test setup.

    Returns
    None
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username=mock_create_user.get("username"),
            password=mock_create_user.get("password"),
            author_pseudonym=mock_create_user.get("author_pseudonym")
        )

        self.book1 = Book.objects.create(
            title="Test Book 1",
            description="This is a test book 1.",
            author=self.user,
            price=10.99,
            published=mock_create_book.get("published")
        )

        self.book2 = Book.objects.create(
            title="Test Book 2",
            description="This is a test book 2.",
            author=self.user,
            price=15.99,
            published=mock_create_book.get("published")
        )
        self.url = reverse('my_book_detail')

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_user_books(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book(self):
        data = {
            'title': 'New Book',
            'description': 'New book description',
            'price': 12.99,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.data['status_code'], status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Book created successfully!')


class ListCreateBooksViewSearchTestCase(APITestCase):
    """
    ListCreateBooksViewSearchTestCase is a test case class for testing the search functionality of
    the ListCreateBooksView API view. The purpose of this test case is to ensure that the search
    feature works as expected and returns accurate results when searching for books by title,
    description, or author pseudonym.

    Parameters
    unittest.TestCase : A base test case class from the unittest module, which provides methods for
    assertions and test setup.

    Returns
    None
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username=mock_create_user.get("username"),
            password=mock_create_user.get("password"),
            author_pseudonym=mock_create_user.get("author_pseudonym")
        )

        self.book1 = Book.objects.create(
            title="Test Book 1",
            description="This is a test book 1.",
            author=self.user,
            price=10.99,
            published=mock_create_book.get("published")
        )

        self.book2 = Book.objects.create(
            title="Test Book 2",
            description="This is a test book 2.",
            author=self.user,
            price=15.99,
            published=mock_create_book.get("published")
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_search_books_description(self):
        self.client.login(
            username=mock_create_user.get("username"),
            password=mock_create_user.get("password")
        )

        url = reverse('my_book_search', kwargs={'pk': self.user.id})
        response = self.client.get(url, {'search': 'test book 1'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book 1')
        self.assertEqual(response.data[0]['description'], 'This is a test book 1.')

    def test_search_books_no_results(self):
        self.client.login(
            username=mock_create_user.get("username"),
            password=mock_create_user.get("password")
        )

        url = reverse('my_book_search', kwargs={'pk': self.user.id})
        response = self.client.get(url, {'search': 'non_existent_book'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class UpdateBookViewTestCase(APITestCase):
    """
    UpdateBookViewTestCase is a test case class for testing the UpdateBookView API view.
    The purpose of this test case is to ensure that the book update functionality works
    as expected and allows authenticated users to update their books' details, such as
    title, description, cover image, and price.

    Parameters
    unittest.TestCase : A base test case class from the unittest module, which provides
    methods for assertions and test setup.

    Returns
    None
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username=mock_create_user.get("username"),
            password=mock_create_user.get("password"),
            author_pseudonym=mock_create_user.get("author_pseudonym")
        )
        self.book = Book.objects.create(
            title=mock_create_book.get("title"),
            description=mock_create_book.get("description"),
            author=self.user,
            price=9.99
        )
        self.url = reverse('my_books_update', args=[self.book.id])
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_update_book(self):
        update_data = {
            'title': 'Updated Test Book',
            'description': 'Updated test book description',
            'price': 12.99
        }
        response = self.client.put(self.url, data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Test Book')
        self.assertEqual(self.book.description, 'Updated test book description')
        self.assertEqual(float(self.book.price), 12.99)

    def test_partial_update_book(self):
        partial_update_data = {
            'title': 'Partial Update Test Book'
        }
        response = self.client.patch(self.url, data=partial_update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Partial Update Test Book')
        self.assertEqual(self.book.description, mock_create_book.get("description"))
        self.assertEqual(float(self.book.price), 9.99)


class UnpublishedBookViewTestCase(APITestCase):
    """
    UnpublishedBookViewTestCase is a test case class for testing the UnpublishedBookView API view.
    The purpose of this test case is to ensure that the book unpublishing functionality works as expected,
    allowing authenticated users to unpublish their books by changing their published status to False.

    Parameters
    unittest.TestCase : A base test case class from the unittest module, which provides methods for assertions
    and test setup.

    Returns
    None
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Darth Vader',
            password='darthpassword',
            author_pseudonym='darthpseudonym'
        )
        self.published_book = Book.objects.create(
            title='Darth Vader publish Test Book',
            description='Published test book description',
            author=self.user,
            price=9.99
        )
        self.unpublished_book = Book.objects.create(
            title='Darth Vader unpublish Test Book',
            description='Unpublished test book description',
            author=self.user,
            price=12.99,
            published=mock_create_book.get("published")
        )
        self.url = reverse('unpublished', args=[self.unpublished_book.id])
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_unpublish_book(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.unpublished_book.refresh_from_db()
        self.assertFalse(self.unpublished_book.published)

    def test_unpublish_already_unpublished_book(self):
        # Unpublish the book before running the test
        self.unpublished_book.unpublish()
        self.unpublished_book.save()

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.unpublished_book.refresh_from_db()
        self.assertFalse(self.unpublished_book.published)


class UnPublishedBookDetailsViewTestCase(APITestCase):
    """
    UnPublishedBookDetailsViewTestCase is a test case class for testing the UnPublishedBookDetailsView API view.
    The purpose of this test case is to ensure that the view retrieves a list of unpublished books for the
    authenticated user, providing accurate information about books that have their published status set to False.

    Parameters
    unittest.TestCase : A base test case class from the unittest module, which provides methods for assertions and
    test setup.

    Returns
    None
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username=mock_create_user.get("username"),
            password=mock_create_user.get("password"),
            author_pseudonym=mock_create_user.get("author_pseudonym")
        )
        self.published_book = Book.objects.create(
            title='Published Test Book',
            description='Published test book description',
            author=self.user,
            price=9.99
        )
        self.unpublished_book = Book.objects.create(
            title='Unpublished Test Book',
            description='Unpublished test book description',
            author=self.user,
            price=12.99,
            published=False
        )
        self.url = reverse('list_unpublished_books')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_unpublished_books(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.unpublished_book.title)

    def test_get_unpublished_books_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookSchemaValidationTestCase(TestCase):
    """
    Test case for validating the Book schema.
    """

    def setUp(self):
        """
        Sets up the Book data dictionary for tests.
        """
        self.book_dict = {
            "title": "The Lord of the Rings",
            "description": "A fantasy novel",
            "author": {"id": 1},
            "cover_image": "https://example.com/book.jpg",
            "price": 9.99,
            "published_on": "2022-04-01T12:00:00Z",
            "published": True
        }

    def test_book_valid_schema(self):
        """
        Tests if the Book data dictionary is valid according to the schema.
        """
        self.book_dict['price'] = str(self.book_dict['price'])
        try:
            jsonschema.validate(self.book_dict, mock_book_schema)
        except jsonschema.exceptions.ValidationError as e:
            self.fail(e)

    def test_title_schema(self):
        """
        Tests if the Book title field validation works properly.
        """
        self.book = Book(
            title=mock_create_book.get("title"),
            description=mock_create_book.get("description"),
            author_id=1,
            price=9.99
        )
        self.book_dict = {
            "title": self.book.title
        }
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(self.book_dict, mock_book_schema)

    def test_description_schema(self):
        """
        Tests if the Book description field validation works properly.
        """
        self.book = Book(
            title=mock_create_book.get("title"),
            description=mock_create_book.get("description"),
            author_id=1,
            price=9.99
        )
        self.book_dict = {
            "description": self.book.description
        }
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(self.book_dict, mock_book_schema)

    def test_author_schema(self):
        """
        Tests if the Book author field validation works properly.
        """
        self.author = CustomUser.objects.create_user(
            username="test_author",
            password="testpassword",
            author_pseudonym="Test Author"
        )
        self.book = Book(
            title=mock_create_book.get("title"),
            description=mock_create_book.get("description"),
            author=self.author,
            price=9.99
        )
        self.book_dict = {
            "author": self.book.author.id
        }
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(self.book_dict, mock_book_schema)

    def test_cover_image_schema(self):
        """
        Tests if the Book cover image field validation works properly.
        """
        self.book = Book(
            title=mock_create_book.get("title"),
            description=mock_create_book.get("description"),
            author_id=1,
            price=9.99
        )
        self.book_dict = {
            "cover_image": "invalid-image-data"
        }
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(self.book_dict, mock_book_schema)

    def test_price_schema(self):
        """
        Tests if the Book price field validation works properly.
        """
        self.book = Book(
            title=mock_create_book.get("title"),
            description=mock_create_book.get("descritpion"),
            author_id=1,
            price=9.99
        )
        self.book_dict = {
            "price": str(self.book.price)
        }
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(self.book_dict, mock_book_schema)
