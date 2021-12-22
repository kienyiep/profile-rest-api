from rest_framework import serializers
"""A serializer is a feature from the django rest framework that allow you to easily convert data inputs into python objects and vice versa.
so if you want to add post or update functionality to our HelloApiView, then we need to create a serializer to receive the content that we post to the API.

"""
from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """Serializers a name field for testing our APIview"""
    """Serializer also validate the content past that api is the correct type , thay you require for that field"""
    name =serializers.CharField(max_length=10)


"""The way you work with the ModelSerializer is you use a meta class to configure the serializer to point to a specific model in our project"""
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    """True, This means you can only use it to create new object or update object, you can't use it to retrieve object"""
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password' : {
                'write_only':True,
                'style': {'input_type' : 'password'}
            }
        }


    def create(self,validated_data):
        """this will overwrite the create method in the view"""
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serialize profile feed items"""
    class Meta:
        model = models.userPhonebook
        """We dont want the user to set the user_profile when they create a new feed item, we want the user profile based on the user that is authenticated
           so we dont want one user able to create a new profile feed item and assign that to another user because it will cause security flaw in the system
           Therefore, we will set this user_profile to the authenticated user and we will make the user profile field read only
           So when we list the object, we can see which users created which feed items, but when we create object,
           it can only be assigned to the current user that is authenticated"""
        fields = ('id','user_profile','phone_username','phone_number','created_on')
        extra_kwargs={'user_profile':{'read_only':True}}
