from random import random
from food import Food


class Foodage:
    RADIUS_EXTREMA = {
        "maximum": 0.1,
        "minimum": 0.0001
    }

    FOOD_PARAMETERS = {
        'energy_per_radius': 50,
    }

    def __init__(self):
        self.food_list = []

    def update(self):
        for food in self.food_list:
            food.update()

    def add_food(self, food):
        self.food_list += [food]

    def add_random_foods(self, number_of_new_foods=10):
        for i in range(number_of_new_foods):
            radius = Foodage.RADIUS_EXTREMA['minimum'] ** 2 + \
                     random() * (Foodage.RADIUS_EXTREMA['maximum'] ** 2 - Foodage.RADIUS_EXTREMA['minimum'] ** 2)
            self.add_food(
                Food(energy=Foodage.FOOD_PARAMETERS['energy_per_radius'] ** 2 * radius * radius, radius=radius))

    def delete_food(self, food):
        self.food_list.remove(food)

    def update_food_gen_parameters(self):
        print('to be updated')
        # TODO update food parameters that exist in environment
