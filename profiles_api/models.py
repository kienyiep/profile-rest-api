from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
"""retrieve the setting from the setting.py file in the profiles_project folder,
the particular setting that we are going to retrieve is the AUTH_USER_MODEL"""


"""Django we use models to describe the data we need for our app ,
django will use the models to set up and configure our database to store our data effectively
Each model in django maps to a specific table within our database.
Django handle the relationship between the model and the database for us so we never need to write the sql statement or interact with the database directly. """


class UserProfileManager(BaseUserManager):
    """Manager for user profile"""

    def create_user(self,email,name,password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        """this will encrypt the password"""
        user.set_password(password)
        """standard procedure for saving object in django """
        user.save(using =self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save the new super user with given details """
        user = self.create_user(email,name,password)
        """The is_superuser is automatically created by the PermissionsMixin"""
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    """This says we want the email coloumn on our UserProfile database table"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length = 255)
    """This will determine whether the user profile is activate or not"""
    is_active = models.BooleanField(default=True)
    """ this will determine whether the user is a staff or not"""
    is_staff = models.BooleanField(default= False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve fullname of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email


class ProfileFeedItem(models.Model):
    """The user profile is the profile that that owns or created the profile feed item"""
    user_profile = models.ForeignKey(

        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    status_text= models.CharField(max_length=255)

    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return self.status_text
# Create your models here.
