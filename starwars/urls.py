"""starwars URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from swapi.api import Planets, Movies, add_remove_favorite_planet, add_remove_favorite_movies
urlpatterns = [
    path('planets/', Planets.as_view({'get': 'list'}), name='planets-list'),
    path('planets/<id>/', Planets.as_view({
        'get': 'retrieve',
    })),
    path('favourite/planets/', add_remove_favorite_planet, name='favorite_planets'),
    path('movies/', Movies.as_view({'get': 'list'}), name='movies-list'),
    path('movies/<id>/', Movies.as_view({
        'get': 'retrieve',
    })),
    path('favourite/movies/', add_remove_favorite_movies, name='favorite_movies')
]
