import json

import requests
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from serializer import PokemonsSchema
from util import retrieve_pokemon_data, validate_pokemon_url_parameter

app = Flask(__name__)


@app.errorhandler(Exception)
def handle_exception(e):
    code = 500
    error = "Internal Server Error"
    if isinstance(e, HTTPException):
        code = e.code
        error = e.name
    app.logger.exception(e)
    return jsonify(error=error), code


@app.route("/search", methods=["GET"])
def query_pokemons():
    try:
        pokemons = validate_pokemon_url_parameter(request.args.get("pokemons"))
    except ValueError as e:
        return jsonify(error=str(e)), 400

    app.logger.info(f"Searching data for the following pokemons: {pokemons}")

    found_pokemons = []
    for pokemon in pokemons:
        data = retrieve_pokemon_data(pokemon)
        if data is not None:
            found_pokemons.append(data)

    if not found_pokemons:
        return jsonify(error="No pokemons found"), 404

    schema = PokemonsSchema()
    return jsonify(schema.dump({"pokemons": found_pokemons}))


if __name__ == "__main__":
    app.run(debug=True)
