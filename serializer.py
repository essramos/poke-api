from random import sample
from statistics import median

from marshmallow import Schema, fields, post_dump


class PokemonSchema(Schema):
    class Meta:
        ordered = True

    name = fields.String()
    height = fields.Float()
    weight = fields.Float()
    color = fields.Method("get_color")
    moves = fields.Method("get_random_moves")
    base_happiness = fields.Method("get_base_happiness")

    def get_random_moves(self, data):
        moves = data.get("moves")
        if len(moves) == 0:
            return []

        random_moves_indices = sample(
            range(len(moves)), k=1 if len(moves) < 2 else 2
        )  # returns list
        return [moves[key].get("move").get("name") for key in random_moves_indices]

    def get_color(self, data):
        return data.get("specie").get("color").get("name")

    def get_base_happiness(self, data):
        return data.get("specie").get("base_happiness")


class PokemonsSchema(Schema):
    pokemons = fields.Nested(PokemonSchema, many=True)

    @post_dump
    def set_average_happiness(self, data, many, **kwargs):
        base_happiness = [
            pokemons.get("base_happiness") for pokemons in data.get("pokemons")
        ]
        if len(base_happiness) > 0:
            data["average_happiness"] = sum(base_happiness) / len(base_happiness)
        else:
            data["average_happiness"] = 0

        return data

    @post_dump
    def set_median_happiness(self, data, many, **kwargs):
        data["median_happiness"] = median(
            [pokemons.get("base_happiness") for pokemons in data.get("pokemons")]
        )
        return data
