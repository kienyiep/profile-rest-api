from django.contrib import admin
from profiles_api import models
# Register your models here.

"""
Enable the django admin for our user profile model
By default, the django admin is already enabled on all new projects however you need to register any newly created model with the django admin,
so it knows that you want to display the model in the admin interface.
"""
"""This tell the django admin to register our user profile model with the admin site so it makes it accessible through the admin interface """
admin.site.register(models.UserProfile)

admin.site.register(models.ProfileFeedItem)
