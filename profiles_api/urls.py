from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles_api import views

"""view set use the router to generate the different route which are available for our view set,
with the view set you may be accessing the list request which is just the route of our API
In this case, you would use a different URL then if you are accessing a specific object to do an update, delete, or a get  """

"""Now, we will create a default router and register our ViewSet with the default router and pass the URLsw  into URL pattern"""
router = DefaultRouter()
"""Becsue the router will create all the four URLs for us, we dont need to specify a forward slash, when we define our view set URL name"""
"""The base name will be used to retrieve the URL in our router if we ever need to do that using the URL retrieving function provided by django """
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
"""At here we dont need the base name argument, this is because a queryset in the UserProfileViewSet,
which can allow the django rest framework to figure out the name from the model """
router.register('profile', views.UserProfileViewSet)
urlpatterns=[
    path('hello-view/', views.HelloApiView.as_view()),
    path('',include(router.urls))
]
""" So as we register the new route with our router, it generates a list of URLs that are associated for our view set it figures out the URLs """
"""that are required for all of the functions that we add to our view set and then it generates this URL list"""
"""which we can pass in using the path function and the include function to our URL patterns"""
"""The reason that the blank string is specified here because we dont want to put a prefix to this URL, we just want to include all of the URLs in the base of this URLs file"""
