from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_image',  default='profile_image/avatar_default.png')
    friends=models.ManyToManyField("self",related_name="friends")
    rate=models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
        
    def str(self):
        return 'Profil użytkownika {}.'.format(self.user.username)
