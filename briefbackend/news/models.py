from django.db import models

# Create your models here.
class Article(models.Model):
	author = models.CharField(max_length=255)
	title = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	url = models.CharField(max_length=255)
	source = models.CharField(max_length=255)
	image = models.CharField(max_length=255)
	category = models.CharField(max_length=255)
	language = models.CharField(max_length=255)
	country = models.CharField(max_length=255)
	published_at = models.CharField(max_length=255)

	class Meta:
		verbose_name_plural = "articles"

	def __str__(self):
			return self.title
