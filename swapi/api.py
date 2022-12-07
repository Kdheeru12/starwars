from rest_framework import viewsets
from rest_framework.response import Response
import requests
from django.conf import settings
from swapi.models import FavouritePlanets, FavouriteMovies
from django.http import JsonResponse
from rest_framework.decorators import api_view


def query(instance, params={}):
    response = requests.get(f"{settings.BASE_URL}/{instance}", params)
    return response.json()


def process_result(url, user, params):
    alias_search = []
    if 'planets' in url:
        favourites = set(FavouritePlanets.objects.filter(user=user).values_list('planet', flat=True))
        if "search" in params:
            alias_search = set(FavouritePlanets.objects.filter(
                user=user,
                alias=params['search']
            ).values_list('planet', flat=True))
        key = 'name'
    elif 'films' in url:

        favourites = set(FavouriteMovies.objects.filter(user=user).values_list('movie', flat=True))
        if "search" in params:
            alias_search = set(
                FavouriteMovies.objects.filter(
                    user=user,
                    alias=params['search']
                ).values_list(
                    'movie',
                    flat=True
                )
            )
        key = 'title'

    results = query(url, params)

    if alias_search and params['search'] in alias_search:
        alias_search.remove(params['search'])

    for search in alias_search:
        search_result = query(url, {"search": search})
        results.get('results').extend(search_result.get('results', []))

    if results.get('results'):
        for result in results['results']:
            if result[key] in favourites:
                result['is_favourite'] = True
            else:
                result['is_favourite'] = False
    return results


class Planets(viewsets.ViewSet):
    
    def list(self, request):

        page = self.request.GET.get('page', 1)
        search = self.request.GET.get('search', None)
        # can be written in permission class to..

        try:
            user = request.META["HTTP_USERID"]
        except Exception:
            user = request.META.get('headers', {}).get("HTTP_USERID")

        if not user:
            return Response({"error": "userid not found in headers"}, status=400)
        if search:
            params = {"search": search}
        else:
            params = {"page": page}
        results = process_result('planets/', user, params)
        return Response(results)

    def retrieve(self, request, *args, **kwargs):
        try:
            user = request.META.get("HTTP_USERID")
        except Exception:
            user = request.META.get('headers', {}).get("HTTP_USERID")
        if not user:
            return Response({"error": "userid not found in headers"}, status=400)
        planet_id = kwargs.get('id')
        results = process_result(f"planets/{planet_id}", user, {})
        return Response(results)


class Movies(viewsets.ViewSet):
    
    def list(self, request):
        page = self.request.GET.get('page', 1)
        search = self.request.GET.get('search', None)
        # can be written in permission class to..

        try:
            user = request.META.get("HTTP_USERID")
        except Exception:
            user = request.META.get('headers', {}).get("HTTP_USERID")
        if not user:
            return Response({"error": "userid not found in headers"}, status=400)
        if search:
            params = {"search": search}
        else:
            params = {"page": page}
        results = process_result('films/', user, params)
        return Response(results)

    def retrieve(self, request, *args, **kwargs):
        try:
            user = request.META.get("HTTP_USERID")
        except Exception:
            user = request.META.get('headers', {}).get("HTTP_USERID")
        if not user:
            return Response({"error": "userid not found in headers"}, status=400)
        film_id = kwargs.get('id')
        results = process_result(f"films/{film_id}", user, {})
        return Response(results)


def add_remove_favorites(name, alias, user, type):
    if name is None:
        return JsonResponse({"error": f"Invalid Payload. {type} required"}, status=400, safe=False)

    payload = {
        "user": user,
        "alias": alias,
    }
    if type == 'planet':
        # check planet exists  in the database
        search = query('planets', {'search': name})
        payload['planet'] = name
        model = FavouritePlanets
    elif type == 'film':
        search = query('films', {'search': name})
        payload['movie'] = name
        model = FavouriteMovies

    if not search['results']:
        return JsonResponse({"error": f"{type} doesn't exists"}, status=400, safe=False)

    # if movie exists remove from favorites
    # can same same movie as favorite with different alias
    check_item = model.objects.filter(**payload)
    if check_item.exists():
        check_item.delete()
        return JsonResponse({"message": f"{type} removed from favourites"}, status=200, safe=False)
    else:
        model.objects.create(**payload)
        return JsonResponse({"message": f"{type} added to favourites"}, status=200, safe=False)


@api_view(['POST', 'GET'])
def add_remove_favorite_planet(request):
    try:
        user = request.META.get("HTTP_USERID")
    except Exception:
        user = request.META.get('headers', {}).get("HTTP_USERID")
    if not user:
        return Response({"error": "userid not found in headers"}, status=400)
    if request.method == 'GET':
        data = list(FavouritePlanets.objects.filter(user=user).values())
        return JsonResponse(data, status=200, safe=False)
    if request.method == 'POST':
        data = request.data

        return add_remove_favorites(data.get('planet'), data.get('alias'), user, 'planet')


@api_view(['POST', 'GET'])
def add_remove_favorite_movies(request):

    try:
        user = request.META.get("HTTP_USERID")
    except Exception:
        user = request.META.get('headers', {}).get("HTTP_USERID")
    if not user:
        return Response({"error": "userid not found in headers"}, status=400)
    if request.method == 'GET':

        data = list(FavouriteMovies.objects.filter(user=user).values())
        return JsonResponse(data, status=200, safe=False)

    if request.method == 'POST':
        data = request.data
        return add_remove_favorites(data.get('movie'), data.get('alias'), user, 'film')
