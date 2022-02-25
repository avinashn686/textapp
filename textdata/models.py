from tkinter import CASCADE
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
import uuid
# Create your models here.
class TextTitle(models.Model):
    object_id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title=models.CharField(max_length=220,unique=True)
class TextTable(models.Model):
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    text=models.TextField()
    title=models.CharField(max_length=220)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    object_id=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    item_text=models.ManyToManyField(TextTitle,blank=True)





    