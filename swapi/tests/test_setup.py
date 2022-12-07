from rest_framework.test import APITestCase
from django.urls import reverse
from swapi.models import FavouriteMovies, FavouritePlanets


class TestSetup(APITestCase):
    def setUp(self):
        self.planets = reverse('planets-list')
        self.movies = reverse('movies-list')
        self.favourite_planets = reverse('favorite_planets')
        self.favourite_movies = reverse('favorite_movies')
        self.favourite_planet = FavouritePlanets.objects.create(user="user-1", planet="Tatooine", alias="newplanet")
        self.favourite_movie = FavouriteMovies.objects.create(user="user-1", movie="A New Hope", alias="newmovie")
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
