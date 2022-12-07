from swapi.tests.test_setup import TestSetup

headers = {"HTTP_USERID": "user-1"}


class PlanetsTestViews(TestSetup):
    def test_get_planets_no_userid(self):
        res = self.client.get(self.planets)
        self.assertEqual(res.status_code, 400)
        self.assertDictEqual(res.json(), {'error': 'userid not found in headers'})

    def test_get_planets(self):
        res = self.client.get(self.planets, **headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['count'], 60)

    def test_get_planets_page_2(self):
        res = self.client.get(self.planets, {'page': 2}, **headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['next'], "https://swapi.dev/api/planets/?page=3")

    def test_get_planet_search(self):
        res = self.client.get(self.planets, {'search': "Eriadu"}, **headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['results']), 1)

    def test_retrive_planet(self):
        res = self.client.get(self.planets+"1/", **headers)
        self.assertEqual(res.status_code, 200)

    def test_search_favouite(self):
        res = self.client.get(self.planets, {'search': self.favourite_planet.alias}, **headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['results']), 1)
        self.assertEqual(res.json()['results'][0]['name'], self.favourite_planet.planet)
        self.assertEqual(res.json()['results'][0]['is_favourite'], True)


class MoviesTestViews(TestSetup):
    def test_get_movies_no_userid(self):
        res = self.client.get(self.movies)
        self.assertEqual(res.status_code, 400)
        self.assertDictEqual(res.json(), {'error': 'userid not found in headers'})

    def test_get_movies(self):
        res = self.client.get(self.movies, **headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['count'], 6)

    def test_get_movies_search(self):
        res = self.client.get(self.movies, {'search': "A New Hope"}, **headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['results']), 1)

    def test_retrive_movies(self):
        res = self.client.get(self.movies+"1/", **headers)
        self.assertEqual(res.status_code, 200)

    def test_search_favouite_movie(self):
        res = self.client.get(self.movies, {'search': self.favourite_movie.alias}, **headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['results']), 1)
        self.assertEqual(res.json()['results'][0]['title'], self.favourite_movie.movie)
        self.assertEqual(res.json()['results'][0]['is_favourite'], True)

    def test_user_2_search_favourite(self):
        headers = {"HTTP_USERID": "user-2"}
        res = self.client.get(self.movies, {'search': self.favourite_movie.alias}, **headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['results']), 0)


class AddFavourites(TestSetup):
    def test_no_user_in_fav_movies(self):
        res = self.client.get(self.favourite_movies)
        self.assertEqual(res.status_code, 400)
        self.assertDictEqual(res.json(), {'error': 'userid not found in headers'})

    def test_no_user_in_fav_planets(self):
        res = self.client.get(self.favourite_planets)
        self.assertEqual(res.status_code, 400)
        self.assertDictEqual(res.json(), {'error': 'userid not found in headers'})

    def test_get_fav_planets(self):
        res = self.client.get(self.favourite_planets, **headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 1)

    def test_get_fav_movies(self):
        res = self.client.get(self.favourite_movies, **headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 1)

    def test_get_fav_movies_user_2(self):
        headers = {"HTTP_USERID": "user-2"}
        res = self.client.get(self.favourite_movies, **headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 0)

    def test_add_fav_movie(self):
        res = self.client.post(self.favourite_movies, {
            "movie": "The Empire Strikes Back",
            "alias": "somename"
        }, **headers)
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.json(), {'message': 'film added to favourites'})

    def test_remove_fav_movie(self):
        res = self.client.post(self.favourite_movies, {
            "movie": self.favourite_movie.movie,
            "alias": self.favourite_movie.alias
        }, **headers)
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.json(), {'message': 'film removed from favourites'})

    def test_add_fav_planet(self):
        res = self.client.post(self.favourite_planets, {
            "planet": "Alderaan",
            "alias": "somename"
        }, **headers)
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.json(), {'message': 'planet added to favourites'})

    def test_remove_fav_planet(self):
        res = self.client.post(self.favourite_planets, {
            "planet": self.favourite_planet.planet,
            "alias": self.favourite_planet.alias
        }, **headers)
        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.json(), {'message': 'planet removed from favourites'})

    def test_planet_not_found(self):
        res = self.client.post(self.favourite_planets, {
            "planet": "randomname",
            "alias": self.favourite_planet.alias
        }, **headers)
        self.assertEqual(res.status_code, 400)
        self.assertDictEqual(res.json(), {"error": "planet doesn't exists"})

    def test_movie_not_found(self):
        res = self.client.post(self.favourite_movies, {
            "movie": "randomname",
            "alias": self.favourite_planet.alias
        }, **headers)
        self.assertEqual(res.status_code, 400)
        self.assertDictEqual(res.json(), {"error": "film doesn't exists"})

    def test_invalid_payload(self):
        res = self.client.post(self.favourite_movies, {
            "something": "randomname",
            "alias": self.favourite_planet.alias
        }, **headers)
        self.assertEqual(res.status_code, 400)
