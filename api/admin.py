from django.contrib import admin

from api.models import Anime, Character

# Register your models here.


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('name', 'year_began', 'year_ended')


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'anime')
