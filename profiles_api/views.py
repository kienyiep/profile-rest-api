from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
"""the status object from the rest framework is a list of handly http status codes that you can use when returning responses from your API."""
from profiles_api import serializers
"""We will use this to tell the API what data to expect while making post,put and patch to our requests to our api"""
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
         return Response({'methos':'PUT'})

    def patch(self,request,pk=None):
          """Handle a partial update of an object, updating the field that is provided in the request"""
          return Response({'methos':'PATCH'})

    def delete(self,request,pk=None):
          """Delete an object"""
          return Response({'method':'DELETE'})
