# A single GET endpoint to retrieve your 5 most favortite pokemon!

## Dependencies

### Python

1. install python 3.8 and set up and activate a virtual environment
2. `pip install -r requirements.txt`

## Run server

`python main.py`

## Run tests

`pytest`

## How to search for pokemons

Pass in 5 pokemons to `pokemons` URL parameter, comma delimeted  
Example:

```
curl -X GET \
  'http://127.0.0.1:5000/search?pokemons=pikachu,gible,mew,mewtwo,squirtle' \
  -H 'Postman-Token: 453cff9e-9196-4531-a9ea-da5cd7f306e6' \
  -H 'cache-control: no-cache'
```

- Pokemons not found will not exists in the response.
- If you pass > 5 pokemon names, it will return 400 error.
- Duplicated pokemon names will be deduped

```
{
    "pokemons": [
        {
            "name": "gible",
            "height": 7.0,
            "weight": 205.0,
            "color": "blue",
            "moves": [
                "substitute",
                "sandstorm"
            ],
            "base_happiness": 50
        },
        {
            "name": "squirtle",
            "height": 5.0,
            "weight": 90.0,
            "color": "blue",
            "moves": [
                "aura-sphere",
                "blizzard"
            ],
            "base_happiness": 50
        },
        {
            "name": "pikachu",
            "height": 4.0,
            "weight": 60.0,
            "color": "yellow",
            "moves": [
                "iron-tail",
                "double-edge"
            ],
            "base_happiness": 50
        },
        {
            "name": "mewtwo",
            "height": 20.0,
            "weight": 1220.0,
            "color": "purple",
            "moves": [
                "life-dew",
                "confide"
            ],
            "base_happiness": 0
        },
        {
            "name": "mew",
            "height": 4.0,
            "weight": 40.0,
            "color": "pink",
            "moves": [
                "hydro-cannon",
                "hyper-beam"
            ],
            "base_happiness": 100
        }
    ],
    "average_happiness": 50.0,
    "median_happiness": 50
}
```

## Next Steps (Productionize the app)

- Productionize Flask set-up (like using Application factories)
- Use production WSGI server like Gunicorn
- Possibly cache results from calling Pokemon API
- Add swagger docs to help document endpoints
- Dockerize the app so we can easily deploy to Cloud services like AWS
