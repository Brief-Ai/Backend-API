from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
	author = models.CharField(max_length=255, null=True)
	title = models.CharField(max_length=255)
	description = models.TextField()
	# Prevent issues with to long urls so dont use models.CharField(max_length=255)
	url = models.TextField()
	source = models.CharField(max_length=255)
	# Prevent issues with to long urls so dont use CharField(max_length=255, null=True)
	image = models.TextField(null=True)
	category = models.CharField(max_length=255, null=True)
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
