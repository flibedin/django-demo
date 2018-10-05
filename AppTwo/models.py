from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cliente( models.Model):
    first_name = models.CharField( max_length=30 )
    last_name = models.CharField( max_length=30 )
    email = models.CharField( max_length=64 )

    def __str__( self ):
        return self.first_name + " " +  self.last_name

class UserProfileInfo( models.Model ):
    user = models.OneToOneField( User, on_delete=models.CASCADE )

    portfolio = models.URLField( blank=True )
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__( self ):
        return self.user.username
