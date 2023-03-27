from unittest.mock import patch

import pytest
import requests
from main import app
from util import call_pokemon_api, retrieve_pokemon_data


class TestRetrievePokemonData:
    @patch("util.call_pokemon_api")
    def test_retrieve_pokemon_data_with_valid_response(self, mock_call_pokemon_api):
        mock_call_pokemon_api.side_effect = [
            ({"foo": "bar"}, 200),
            ({"bar": "foo"}, 200),
        ]
        with app.app_context():
            expected_result = {"foo": "bar", "specie": {"bar": "foo"}}
            assert retrieve_pokemon_data("pikachu") == expected_result

    @patch("util.call_pokemon_api")
    def test_retrieve_pokemon_data_with_none_response(self, mock_call_pokemon_api):
        mock_call_pokemon_api.side_effect = [
            (None, 404),
        ]
        with app.app_context():
            assert retrieve_pokemon_data("pikachu") is None
            mock_call_pokemon_api.assert_called_once()

    @patch("util.call_pokemon_api")
    def test_retrieve_pokemon_data_with_missing_specie_data(
        self, mock_call_pokemon_api
    ):
        mock_call_pokemon_api.side_effect = [
            ({"foo": "bar"}, 200),
            (None, 404),
        ]
        with app.app_context():
            assert retrieve_pokemon_data("pikachu") is None
            assert mock_call_pokemon_api.call_count == 2


class TestCallPokemonApi:
    def test_call_pokemon_api_successful(self):
        with patch.object(requests, "get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"name": "pikachu"}
            url = "https://someurl.com/pikachu"
            response, status_code = call_pokemon_api(url)
            assert response == {"name": "pikachu"}
            assert status_code == 200
            mock_get.assert_called_with(url)

    def test_call_pokemon_api_failed(self):
        with patch.object(requests, "get") as mock_get:
            mock_get.return_value.status_code = 404
            url = "https://someurl.com/invalid-pokemon"
            response, status_code = call_pokemon_api(url)
            assert response is None
            assert status_code == 404
            mock_get.assert_called_with(url)

    def test_call_pokemon_api_request_exception(self):
        with patch.object(requests, "get") as mock_get:
            mock_get.side_effect = Exception("Some exception occurred")
            with pytest.raises(Exception):
                url = "https://someurl.com/pikachu"
                call_pokemon_api(url)
                mock_get.assert_called_with(url)
