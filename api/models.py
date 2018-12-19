from django.core.exceptions import ValidationError
from django.db import models

from taggit.managers import TaggableManager
# Create your models here.


class Anime(models.Model):
    name = models.CharField(max_length=100, unique=True)
    year_began = models.PositiveSmallIntegerField()
    year_ended = models.PositiveSmallIntegerField(null=True)
    synopsis = models.TextField()
    genres = TaggableManager()

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

        if self.year_ended and (self.year_ended < self.year_began):
            raise ValidationError('year_ended cannot be before year_began')

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

    class Meta:
        unique_together = ('name', 'anime')

    def __str__(self):
        return self.name

