from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions

# Create your views here.

class HelloApiView(APIView):
    """test api view"""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """return a list of apiview features"""

        an_apiview = [
            'uses http methods as function (get, post, patch, put, delete)',
            'it is similar to a traditional django view',
            'gives you the most control over your logic',
            'it is mapped manually to urls'
        ]

        return Response({'message': 'salam', 'an_apiview': an_apiview})

    def post(self, request):
        """create a hello message with our name"""

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """handles updating an object"""

        return Response({'method': 'put'})

    def patch(self, request, pk=None):
        """patch request, only updates fields provided in the request"""

        return Response({'method': 'patch'})

    def delete(self, request, pk=None):
        """deletes an object"""

        return Response({'method': 'delete'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message."""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLS using Routers',
            'Provides more functionality with less code'
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """create a new hello message"""

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """handles getting an object by its id"""

        return Response({'http_method': 'get'})

    def update(self, request, pk=None):
        """handles updating an object"""

        return Response({'http_method': 'put'})

    def partial_update(self, request, pk=None):
        """handles updating part of an object"""

        return Response({'http_method': 'patch'})

    def destroy(self, request, pk=None):
        """handles removing an object"""

        return Response({'http_method': 'delete'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """handles creating , creating and updating profiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class LoginViewSet(viewsets.ViewSet):
    """checks email and password and returns an auth token"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """use the ObtainAuthToken apiview to validate and create a token"""

        return ObtainAuthToken().post(request)


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """handles creating , creating and updating profile feed items"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated,)

    def perform_create(self, serializer):
        """sets the user profile to the logged in user"""

        serializer.save(user_profile=self.request.user)
