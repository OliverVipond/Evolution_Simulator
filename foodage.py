from random import random
from food import Food


class Foodage:
    def __init__(self):
        self.food_list = []

    def update(self):
        for food in self.food_list:
            food.update()

    def add_food(self, food):
        self.food_list += [food]

    def add_random_foods(self, number_of_new_foods=1):
        for i in range(number_of_new_foods):
            calories = random()
            self.add_food(Food(energy=calories * calories, radius=calories / 50))

    def delete_food(self, food):
        self.food_list.remove(food)
