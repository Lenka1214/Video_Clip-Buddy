# Create your models here.
# Inside models.py
from __future__ import unicode_literals
from django.db import models
# Create your models here.
class User(models.Model):
    full_name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    bday=models.DateTimeField(auto_now_add = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Quote(models.Model):
    quoted_by = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    users_likers = models.ManyToManyField(User, related_name="favorites")
    created_by = models.ForeignKey(User,related_name="creator")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
