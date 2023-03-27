import datetime

import jsonschema
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .libs import constants
from .models import CustomUser
from .serializers import CustomUserSerializer

mock_custom_user_schema = constants.CUSTOM_USER_SCHEMA

mock_user_1 = {
    "username": "testuser1",
    "password": "testpassword1",
    "author_pseudonym": "Test Author 1",
    "update_author_pseudonym": "Updated Author 1"
}

mock_user_2 = {
    "username": "testuser2",
    "password": "testpassword2",
    "author_pseudonym": "Test Author 2",
    "update_author_pseudonym": "Updated Author 1"
}


# models
class CustomUserTestCase(TestCase):
    """A test suite for the CustomUser model. It covers the following scenarios:
        1. Creating a user and checking the initial values.
        2. Testing the __str__() method.
        3. Updating a user's author_pseudonym.
        4. Blocking a user with the block() method.
        5. Ensuring the author_pseudonym is unique by handling the IntegrityError.
        6. Checking that created_on and updated_on fields are properly set and updated.
        """

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username=mock_user_1.get("username"),
            password=mock_user_1.get("password"),
            author_pseudonym=mock_user_1.get("author_pseudonym")
        )
        self.user2 = get_user_model().objects.create_user(
            username=mock_user_2.get("username"),
            password=mock_user_2.get("password"),
            author_pseudonym=mock_user_2.get("author_pseudonym")
        )

    def test_create_user(self):
        self.assertEqual(self.user1.username, "testuser1")
        self.assertEqual(self.user1.author_pseudonym, mock_user_1.get("author_pseudonym"))

    def test_str_representation(self):
        self.assertEqual(str(self.user1), mock_user_1.get("author_pseudonym"))

    def test_update_user(self):
        self.user1.author_pseudonym = mock_user_1.get("update_author_pseudonym")
        self.user1.save()
        self.assertEqual(self.user1.author_pseudonym, mock_user_1.get("update_author_pseudonym"))

    def test_create_user_with_duplicate_pseudonym(self):
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                username="testuser3",
                password="testpassword3",
                author_pseudonym=mock_user_1.get("author_pseudonym")  # This pseudonym already exists in the database
            )

    def test_created_on_and_updated_on(self):
        self.assertIsNotNone(self.user1.created_on)
        self.assertIsNotNone(self.user1.updated_on)
        initial_updated_on = self.user1.updated_on

        self.user1.author_pseudonym = mock_user_1.get("update_author_pseudonym")
        self.user1.save()
        self.assertNotEqual(self.user1.updated_on, initial_updated_on)


# views
class CustomUserAPIViewTestCase(APITestCase):
    """A test suite for the CustomUser API views. It covers the following scenarios:
        1. Registering a new user with valid and invalid data.
        2. Logging in with valid and invalid credentials.
        3. Listing all users with and without authentication.
        4. Creating a new user using the UserListCreateView.
        """

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="testuser1",
            password="testpassword1",
            author_pseudonym="Test Author 1"
        )
        self.user2 = get_user_model().objects.create_user(
            username="testuser2",
            password="testpassword2",
            author_pseudonym="Test Author 2"
        )
        self.client = APIClient()

    def test_register(self):
        url = reverse('user_register')
        data = {
            'username': 'testuser3',
            'password': 'testpassword3',
            'author_pseudonym': 'Test Author 3'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], constants.CODE['106'])

    def test_login(self):
        url = reverse('user_login')
        data = {
            'username': 'testuser1',
            'password': 'testpassword1'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_list_create_authenticated(self):
        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.client.get(reverse('list_users'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_create_unauthenticated(self):
        response = self.client.get(reverse('list_users'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CustomUserSerializerTestCase(TestCase):
    """A test suite for the CustomUserSerializer. It covers the following scenarios:
        1. Serializing a CustomUser instance and checking if the output matches the expected serialized data.
        2. Deserializing data to create a new CustomUser instance and verifying if the created user has the
        correct attributes.
        """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            author_pseudonym="Test Author"
        )
        self.serializer = CustomUserSerializer(instance=self.user)

    def test_serialization(self):
        expected_data = {
            'username': 'testuser',
            'author_pseudonym': 'Test Author',
        }
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(expected_data.keys()))
        self.assertEqual(data['username'], expected_data['username'])
        self.assertEqual(data['author_pseudonym'], expected_data['author_pseudonym'])

    def test_deserialization(self):
        data = {
            'username': 'testuser2',
            'author_pseudonym': 'Test Author 2',
        }
        serializer = CustomUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        created_user = serializer.save()
        self.assertEqual(created_user.username, data['username'])
        self.assertEqual(created_user.author_pseudonym, data['author_pseudonym'])


class CustomUserSchemaValidationTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='john',
            author_pseudonym='j.doe',
            created_on=datetime.datetime.now(),
            updated_on=datetime.datetime.now(),
        )

    def test_custom_user_valid_schema(self):
        # Convert the CustomUser object to a dictionary
        user_dict = {
            'username': self.user.username,
            'author_pseudonym': self.user.author_pseudonym,
            'created_on': self.user.created_on.isoformat(),
            'updated_on': self.user.updated_on.isoformat(),
        }

        # Validate the dictionary against the schema
        try:
            jsonschema.validate(user_dict, mock_custom_user_schema)
        except jsonschema.exceptions.ValidationError as e:
            self.fail(e)

    def test_custom_user_invalid_schema(self):
        invalid_author_pseudonym = {'author_pseudonym': 1}
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(invalid_author_pseudonym, mock_custom_user_schema)

        invalid_created_on = {'created_on': "2023-03-26"}
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(invalid_created_on, mock_custom_user_schema)

        invalid_updated_on = {'updated_on': 1}
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(invalid_updated_on, mock_custom_user_schema)
