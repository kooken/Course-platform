from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
NULLABLE = {'null': True,
            'blank': True}

class User(AbstractUser):
    phone = models.CharField(max_length=35, verbose_name='phone', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='avatar', **NULLABLE)
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    city = models.CharField(max_length=100, verbose_name='city', **NULLABLE)

    token = models.CharField(max_length=100, verbose_name='token', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email