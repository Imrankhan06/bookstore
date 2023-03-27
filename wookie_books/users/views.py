from django.contrib.auth import authenticate
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .libs import constants
from .models import CustomUser
from .serializers import CustomUserSerializer


class RegisterView(APIView):
    """
    RegisterView is a Django REST framework APIView that handles user registration.
    It takes the following input parameters in the POST request:

    Parameters:
        request (rest_framework.request.Request): A Django REST framework request object,
                                                  containing 'username', 'password', and
                                                  'author_pseudonym' fields.

    Returns:
        rest_framework.response.Response: A response containing a success message if the
                                          registration is successful, or an error message
                                          with a corresponding error code if the registration fails.

    The view checks for the presence of the required fields and validates that the
    username and author_pseudonym are unique. If the input data is valid, a new
    CustomUser instance is created, and a success message is returned.

    If the input data is not valid or if the username or author_pseudonym already
    exists, an error message with a corresponding error code is returned.
    """

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        author_pseudonym = request.data.get('author_pseudonym')

        if not username:
            return Response({'error': constants.CODE.get('101')}, status=400)
        if not password:
            return Response({'error': constants.CODE.get('102')}, status=400)
        if not author_pseudonym:
            return Response({'error': constants.CODE.get('103')}, status=400)

        # Check if author_pseudonym already exists
        if CustomUser.objects.filter(author_pseudonym=author_pseudonym).exists():
            return Response({'error': constants.CODE.get('104')}, status=409)

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            return Response({'error': constants.CODE.get('105')}, status=409)

        # Create new user
        CustomUser.objects.create_user(username, password=password, author_pseudonym=author_pseudonym)

        return Response({'message': constants.CODE.get('106')}, status=200)


class LoginView(APIView):
    """
    LoginView is a Django REST framework APIView that handles user authentication.
    It takes the following input parameters in the POST request:

    Parameters:
        request (rest_framework.request.Request): A Django REST framework request object,
                                                  containing 'username' and 'password' fields.

    Returns:
        rest_framework.response.Response: A response containing a JWT access token if the
                                          authentication is successful, or an error message
                                          with a corresponding error code if the authentication fails.

    The view uses Django's built-in authenticate method to verify the provided
    username and password. If the authentication is successful, a JSON Web Token (JWT)
    is generated and returned in the response.

    If the authentication fails due to incorrect username or password, an error
    message with a corresponding error code is returned.
    """

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': constants.CODE.get('107')}, status=401)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'token': access_token})


class UserListCreateView(generics.ListCreateAPIView):
    """
    UserListCreateView is a Django REST framework ListCreateAPIView that allows
    authenticated users to retrieve a list of all CustomUser instances or create
    a new CustomUser instance.

    Parameters:
        request (rest_framework.request.Request): A Django REST framework request object.

    Returns:
        For GET requests:
            rest_framework.response.Response: A response containing a list of serialized CustomUser instances.
        For POST requests:
            rest_framework.response.Response: A response containing the serialized CustomUser instance that was created,
                                              or an error message if the input data is not valid.

    The view uses the CustomUserSerializer to serialize and deserialize CustomUser
    instances. The queryset includes all CustomUser instances, and the view
    requires the user to be authenticated in order to access the list and create
    new users.

    When accessed with a GET request, the view returns a list of CustomUser
    instances. When accessed with a POST request, the view creates a new CustomUser
    instance based on the provided input data.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
