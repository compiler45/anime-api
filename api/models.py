from django.db import models

from taggit.managers import TaggableManager
# Create your models here.


class Anime(models.Model):
    name = models.CharField(max_length=100)
    year_began = models.SmallIntegerField()
    year_ended = models.SmallIntegerField()
    synopsis = models.TextField()
    genres = TaggableManager()
    
    def __str__(self):
        return self.name

class Character(models.Model):
    GENDERS = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDERS)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE,
                              related_name='characters')

    def __str__(self):
        return self.name

