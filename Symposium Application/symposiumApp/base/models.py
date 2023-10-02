from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class User(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique = True)
    phoneno = models.CharField(max_length=10)
    year = models.CharField(max_length=20,null=True)
    department = models.CharField(max_length=100,null=True)
    section = models.CharField(max_length=5,null=True)
    regno = models.CharField(max_length=100,null=True)


# class Userpayment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     payment = models.BooleanField(default=False)

class Events(models.Model):
    eventname = models.CharField(max_length=100)
    limit = models.IntegerField()

# class UserEvents(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     email = models.EmailField(unique = True)
#     eventstatus = ArrayField(models.CharField(max_length=100),size=8)


# class TeamEvents(models.Model):
#     eventname = models.CharField(max_length=100)
#     teamname = models.CharField(max_length=200)
#     teammates = ArrayField(models.CharField(max_length=100))
#     password = models.IntegerField()

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Check if size is not already set
#         if not self.teammates.field.size:
#             # Fetch the size from MyModel2 based on the eventname in this model
#             try:
#                 size_from_events = Events.objects.get(eventname=self.eventname).limit
#                 self.teammates.field.size = size_from_events
#             except Events.DoesNotExist:
#                 pass



    