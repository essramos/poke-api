import json

import requests
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from serializer import PokemonsSchema
from util import retrieve_pokemon_data

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
    pokemons = request.args.get("pokemons")
    try:
        pokemons = set(
            [x for x in pokemons.split(",") if x != ""]
        )  # unique pokemons only
    except Exception as e:
        app.logger.exception(e)
        return jsonify(error="Invalid query parameter"), 400

    if not pokemons:
        return jsonify(error="Invalid query parameter"), 400

    if len(pokemons) > 5:
        return jsonify(error="Please pass 5 pokemons only"), 400

    app.logger.info(f"Searching data for the following pokemons: {pokemons}")

    found_pokemons = []
    for pokemon in pokemons:
        data = retrieve_pokemon_data(pokemon)
        if data is not None:
            found_pokemons.append(data)

    if not found_pokemons:
        return jsonify(error="No pokemons found"), 404

    schema = PokemonsSchema()
    return schema.dumps({"pokemons": found_pokemons})


if __name__ == "__main__":
    app.run(debug=True, port=4999)
