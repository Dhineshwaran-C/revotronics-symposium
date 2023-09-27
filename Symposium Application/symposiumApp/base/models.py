from django.db import models
import uuid


# Create your models here.
class User(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique = True)
    phoneno = models.CharField(max_length=10)

class Userpayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.BooleanField(default=False)
    