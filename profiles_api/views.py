from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
"""The token authentication is the type of the authentication for the user to authenticate themselve with our API, it works by generating a random token string when the user log in
and then every request we make to their API that we need to authenticate, we add this token string to the request, and that is effectively a password to check that every request made is authenticated correctly """
from rest_framework.authentication import TokenAuthentication
"""the status object from the rest framework is a list of handly http status codes that you can use when returning responses from your API."""
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
"""This will ensure that the viewset is read only if the user is not authenticated"""
"""from rest_framework.permissions import IsAuthenticatedOrReadOnly"""
"""We use IsAuthenticated only which will block access to the entire endpoint unless the user is authenticated, only the authenticated user can view it"""
from rest_framework.permissions import IsAuthenticated
from profiles_api import serializers
"""We will use this to tell the API what data to expect while making post,put and patch to our requests to our api"""
from profiles_api import models
from profiles_api import permissions

class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer
    def get(self,request,format=None):
        """Return a list of APIViews features"""
        an_apiview =[
        'Uses HTTP methods as function (get,post,patch,put,delete)',
        'Is similar to a traditional Django View',
        'Give you the most control over the application logic',
        'It mapped manually to URLs',
        ]
        """inconvert the response object to json, so it need to return a dictionary"""
        return Response({'message':'Hello!','an_apiview':an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        """serializer class is a function that comes with the APIView that retrieves the configured serializer for our view"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
              name = serializer.validated_data.get('name')
              """this retrieve the name field that we define in the serializer"""
              message = f'Hello {name}'
              return Response({'message':message})
        else:
            return Response(
            serializer.errors,
            status= status.HTTP_400_BAD_REQUEST
             )

    def put(self,request,pk=None):
         """Handle updating an object, by replacing the object with the object provided"""
         return Response({'method':'PUT'})

    def patch(self,request,pk=None):
          """Handle a partial update of an object, updating the field that is provided in the request"""
          return Response({'method':'PATCH'})

    def delete(self,request,pk=None):
          """Delete an object"""
          return Response({'method':'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer
    def list(self,request):
        """Return a hello message"""
        a_viewset =[
        'Uses actions(list,create,retrieve, update,partial update)',
        'Automatically maps to URLs using Routers',
        'Provides more functionality with less code'

        ]
        return Response({'message':'Hello!','a_viewset':a_viewset})

    def create(self,request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
            serializer.errors,
            status= status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method' : 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self,request,pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})

"""The way you using the ModelViewSet is you connect it up to a serializer class"""
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    """The query set will be provided to the modelViewSet so it knows which object in the database are going to be managed through this view set"""
    """The django knows the functions that you want to perform on a model view set,
    which are the create function, list function, update, partial_update and destroy to manage specific model objects in the database. """
    """django framework take care all of this for us just by assigning the serializer class """
    queryset= models.UserProfile.objects.all()
    authentication_classes=(TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    """The permission classes is set to see whether the user gets permission to do certain things  """
    filter_backends = (filters.SearchFilter,)
    """This will mean that the django rest framework will allow us to search for items in this view set by the name or email field"""
    search_fields = ('name','email', )

"""token authentication will generate a random string when you login and then every request you made to the API that you wish yo authenticate, you include the token in the header"""
class UserLoginApiView(ObtainAuthToken):
      """Handle creating user authentication tokens"""
      renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
      """this will add the renderer class to our obtain auth token view which will enable it in the django admin, as the auth token doesn't have the renderer class by default so we need to add it manually"""

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handle  creating, reading and updating profiles feed items"""
    authentication_classes =(TokenAuthentication, )
    serializer_class = serializers.ProfileFeedItemSerializer
    """So we will manage all of our profile feed item objects from our model in our view set"""
    queryset = models.ProfileFeedItem.objects.all()
    """So this set up a basic model viewset that allow us to create and manage feed item objects in the database"""
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated
    )

    def perform_create(self,serializer):
            """Set the user profile to the logged in user"""
            serializer.save(user_profile= self.request.user)
