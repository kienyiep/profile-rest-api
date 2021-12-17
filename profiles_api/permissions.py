from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow the user to edit their own profiles"""
    def has_object_permission(self,request,view,obj):
        """check user is trying to edit their own profile"""
        """We will check the method that is made for the request, we will check whether the method is in the safe method list.
        The method can be HTTP, GET, put, patch or DELETE request.
        The safe methods are the methods that dont require or dont make any changes to the objects
        For example, HTTP GET.
        So we want to allow the user to view other user profile and only can make changes to their own profile.
        """
        if request.method in permissions.SAFE_METHODS:
            """If the method used is a HTTP GET, then it will be in the safe methods, therefore it will just return true and allow the request"""
            return True


        """when you authenticated a request in django rest framework, it will assign the authenticated user profile to the request
         and we can use it to compare with the object that is being updated and make sure they have the same ID """
        return obj.id == request.user.id
        """This way it will return true if the user is trying to update their own profile or otherwise it will return false"""

        """If the user try to do a HTTP PUT to update an object
        we will need to check whether the object which will be
        updating matches to the user authenticated user profile that is added to the authentication of the request"""

class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""
    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id  == request.user.id
