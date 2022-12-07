from django.db import models


class FavouriteMovies(models.Model):
    user = models.CharField(max_length=150)
    alias = models.CharField(max_length=150, blank=True, null=True)
    movie = models.CharField(max_length=150)
    created_on = models.DateTimeField(auto_now_add=True)


class FavouritePlanets(models.Model):
    user = models.CharField(max_length=150)
    alias = models.CharField(max_length=150, blank=True, null=True)
    planet = models.CharField(max_length=150)
    created_on = models.DateTimeField(auto_now_add=True)
