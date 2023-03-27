import json
from unittest.mock import MagicMock, patch

import pytest

from main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


class TestQueryPokemonEndpoint:
    def test_invalid_url(self, client):
        response = client.get("/foo")
        assert response.status_code == 404

    def test_query_pokemons_invalid_parameter(self, client):
        response = client.get("/search?pokemons=,,")

        assert response.status_code == 400
        assert response.json == {"error": "Invalid query parameter"}

    def test_query_pokemons_more_than_five_pokemons(self, client):
        response = client.get(
            "/search?pokemons=pikachu,raichu,charmander,squirtle,venusaur,bulbasaur"
        )

        assert response.status_code == 400
        assert response.json == {"error": "Please pass 5 pokemons only"}

    def test_query_pokemons_no_pokemons_found(self, client):
        with patch("main.retrieve_pokemon_data", return_value=None):
            response = client.get(
                "/search?pokemons=pikachu,charmander,squirtle,eevee,bulbasaur"
            )

            assert response.status_code == 404
            assert response.json == {"error": "No pokemons found"}

    def test_query_pokemons_valid(self, client):
        mock_retrieve_pokemon_data = MagicMock()
        mock_retrieve_pokemon_data.side_effect = [
            {
                "name": "pikachu",
                "height": 1.0,
                "weight": 10.0,
                "moves": [
                    {
                        "move": {
                            "name": "mega-punch",
                        }
                    },
                    {
                        "move": {
                            "name": "pay-day",
                        }
                    },
                ],
                "specie": {"color": {"name": "yellow"}, "base_happiness": 43},
            }
        ]
        with patch("main.retrieve_pokemon_data", mock_retrieve_pokemon_data):
            response = client.get("/search?pokemons=pikachu")
            assert response.status_code == 200
            response = json.loads(response.get_data())
            moves = response.get("pokemons")[0].pop("moves")
            assert response == {
                "pokemons": [
                    {
                        "name": "pikachu",
                        "height": 1.0,
                        "weight": 10.0,
                        "color": "yellow",
                        "base_happiness": 43,
                    }
                ],
                "average_happiness": 43.0,
                "median_happiness": 43,
            }
            # separate test since we cant easily check for equality in list
            assert set(moves) == set(["mega-punch", "pay-day"])
