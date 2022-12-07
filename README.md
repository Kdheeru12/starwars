
## Installing the Deps & Running the application (Tested using Python 3.9.0)

```
virtualenv -p python3 venv

source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```


* /planets/ -> list of planets, search planets by passing search parameter as query parameter(/planets/?search=name)
* /planets/{id}/ -> retrieve planet based on id 
* /favourite/planets/ -> add or remove favourite planet 
    * GET -> list of all favourite planets
    * POST -> add or remove favourite (payload:{
            "planet": "name",
            "alias":  "customname"
        })

* /movies/ -> list of movies, search planets by passing search parameter as query parameter(/movies/?search=name)

* /movies/{id}/ -> retrieve movie based on id 
* /favourite/movies/ -> add or remove favourite movie 
    * GET -> list of all favourite movies
    * POST -> add or remove favourite (payload:{
            "movie": "title",
            "alias":  "customname"
        })


### Note:- required userid in headers in order for the apis to work

## Running Tests
* coverage report 90 %

```python
coverage run --source . -m pytest
```

generate coverage report using ```coverage report```

generate coverage html using ```coverage html```
