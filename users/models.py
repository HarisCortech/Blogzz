import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

# Custom User Model, so we can identify through email
class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"),unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    #Defining the Custom Manger for our Custom User
    objects = CustomUserManager()
    
    # THiis will be automatically called when we create a user
    def __str__(self):
        return self.email


# slugifying the filename so it can stored in products folder, in a url form
# get_image_field = Dynamically generates  a file path for the uploaded image, incorporating  the user's username
# instance and filename = Automatically provided by Django when a file is uploaded via the image field
def get_image_field(instance, filename):
    name = instance.user.username
    slug = slugify(name)
    return f"products/{slug}-{filename}"


# creating a model for profile of our custom user
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    avatar = models.ImageField(upload_to=get_image_field, blank = True)
    bio = models.CharField(max_length=300, blank=True)
    
    def __str__(self):
        return self.user.email
    
    @property
    def filename(self):
        return os.path.basename(self.avatar.name)