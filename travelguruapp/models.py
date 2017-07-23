from __future__ import unicode_literals

from django.db import models

# Create your models here.
class General (models.Model):
	created = models.DateTimeField(auto_now_add=True)
	price = models.CharField(max_length=100, blank=False, null=True)
	price_detail = models.CharField(max_length = 500, blank=False, null=True)
	promotion_one = models.CharField(max_length = 500, blank=False, null=True)
	promotion_two = models.CharField(max_length = 500, blank=False, null=True)

class Place (models.Model):
	created = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=100, blank=False)
	description = models.CharField(max_length=500, blank=False, null=True)

class Image (models.Model):
	created = models.DateTimeField(auto_now_add=True)
	url = models.CharField(max_length=200, blank=False)

class Rate (models.Model):
	created = models.DateTimeField(auto_now_add=True)
	rate = models.CharField(max_length=100, blank=True)