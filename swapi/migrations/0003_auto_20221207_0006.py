# Generated by Django 2.2.25 on 2022-12-07 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swapi', '0002_auto_20221207_0004'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FavouriteMovie',
            new_name='FavouriteMovies',
        ),
        migrations.RenameModel(
            old_name='FavouritePlanet',
            new_name='FavouritePlanets',
        ),
    ]