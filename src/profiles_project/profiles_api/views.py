from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class HelloApiView(APIView):
    """test api view"""

    def get(self, request, format=None):
        """return a list of apiview features"""

        an_apiview = [
            'uses http methods as function (get, post, patch, put, delete)',
            'it is similar to a traditional django view',
            'gives you the most control over your logic',
            'it is mapped manually to urls'
        ]

        return Response({'message': 'salam', 'an_apiview': an_apiview})
