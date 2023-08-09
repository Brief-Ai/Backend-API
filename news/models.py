from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
	author = models.CharField(max_length=255)
	title = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	url = models.CharField(max_length=255)
	source = models.CharField(max_length=255)
	image = models.CharField(max_length=255, null=True)
	category = models.CharField(max_length=255)
	language = models.CharField(max_length=255)
	published_at = models.CharField(max_length=255)

	class Meta:
		verbose_name_plural = "articles"

	def __str__(self):
			return self.title

class Search(models.Model):
    user_id = models.CharField(max_length=255, default=None)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user_id = models.CharField(max_length=255, default=None)
    interests = models.TextField(blank=True, default="[]")
