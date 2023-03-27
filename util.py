import requests
from flask import current_app as app
from typing import Optional, Tuple

POKEMON_API_URL = "https://pokeapi.co/api/v2/pokemon"
POKEMON_SPECIE_API_URL = "https://pokeapi.co/api/v2/pokemon-species"


def retrieve_pokemon_data(pokemon_name: str) -> Optional[dict]:
    pokemon_response, status_code = call_pokemon_api(
        f"{POKEMON_API_URL}/{pokemon_name}"
    )
    if pokemon_response is None:
        app.logger.info(
            f"Pokemon {pokemon_name} was not found. Status code: {status_code}"
        )
        return

    specie_response, status_code = call_pokemon_api(
        f"{POKEMON_SPECIE_API_URL}/{pokemon_response.get('id')}"
    )
    if specie_response is None:
        app.logger.info(
            f"Specie detail for {pokemon_name} was not found. Status code: {status_code}"
        )
        return

    pokemon_response.update({"specie": specie_response})
    return pokemon_response


def call_pokemon_api(url: str) -> Tuple[Optional[dict], int]:
    try:
        response = requests.get(url)
    except Exception:
        raise

    if response.status_code == 200:
        return response.json(), response.status_code
    else:
        return None, response.status_code


def validate_pokemon_url_parameter(pokemons_parameter: str) -> set:
    try:
        pokemons = set(
            [x for x in pokemons_parameter.split(",") if x != ""]
        )  # unique pokemons only
    except Exception as e:
        app.logger.exception(e)
        raise ValueError("Invalid query parameter")

    if not pokemons:
        raise ValueError("Invalid query parameter")

    if len(pokemons) > 5:
        raise ValueError("Please pass 5 pokemons only")

    return pokemons
