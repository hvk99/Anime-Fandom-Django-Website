from django.db import models

# Create your models here.

class Genre(models.Model):

	genre = models.CharField(max_length=200)
	summary = models.TextField()
	slug = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = "Genre"

	def __str__(self):
		return self.genre


class Anime(models.Model):

	anime = models.CharField(max_length=200)
	genre = models.ForeignKey(Genre, default=1, verbose_name="Genre", on_delete=models.SET_DEFAULT)
	summary = models.TextField()

	class Meta:
		verbose_name_plural = "Anime"

	def __str__(self):
		return self.anime


class Character(models.Model):

	name = models.CharField(max_length=200)
	skill = models.CharField(max_length=200)
	power = models.PositiveIntegerField()
	description = models.TextField()

	anime = models.ForeignKey(Anime, default=1, verbose_name="Anime", on_delete=models.SET_DEFAULT)
	slug = models.CharField(max_length=200, default=1)

	def __str__(self):
		return self.name
