from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE )
    image = models.ImageField(upload_to='avatars/' , null=True , blank=True)
    realname = models.CharField(max_length=20 , null=True , blank=True)
    email = models.EmailField(unique=True , null=True)
    location = models.CharField(max_length=20 , null=True , blank=True)
    bio = models.TextField(null=True , blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user)
