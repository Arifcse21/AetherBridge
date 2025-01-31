from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

# Create your models here.


class UserModel(AbstractUser):
    uuid = models.UUIDField(default=uuid4, editable=False)
    address = models.TextField()
    phone = models.CharField(max_length=15)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.pk} - {self.username} - {self.uuid.hex}"
