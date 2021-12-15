from rest_framework import serializers
"""A serializer is a feature from the django rest framework that allow you to easily convert data inputs into python objects and vice versa.
so if you want to add post or update functionality to our HelloApiView, then we need to create a serializer to receive the content that we post to the API.

"""
class HelloSerializer(serializers.Serializer):
    """Serializers a name field for testing our APIview"""
    """Serializer also validate the content past that api is the correct type , thay you require for that field"""
    name =serializers.CharField(max_length=10)
