from __future__ import unicode_literals
from django.db import models

class Users(models.Model):
	firstName = models.CharField(max_length = 120)
	lastName = models.CharField(max_length = 120)
	email = models.CharField(max_length = 120)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
