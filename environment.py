from organisms import Organisms
from foodage import Foodage
import numpy as np


class Environment:
    FOOD_PARAMETERS = {
        'time' : 50,
        'number_of_new_foods': 10
    }
    def __init__(self, number_of_blobs=0, starting_food_items=0):
        self.current_time = 0

        self.organisms = Organisms()
        self.organisms.add_random_blobs(number_of_blobs)

        self.foodage = Foodage()
        self.foodage.add_random_foods(starting_food_items)

        self.get_data_callbacks = []

    def process_food_consumption(self):
        food_list = self.foodage.food_list.copy()
        for food in food_list:
            for organism in self.organisms.find_close_organisms(food.bounding_box):
                if organism.radius > food.radius and \
                        np.linalg.norm(food.position - organism.position) < organism.radius + food.radius:
                    organism.eat_food(food)
                    self.foodage.delete_food(food)
                    break

    def iterate(self):
        self.current_time += 1
        self.organisms.update(self.current_time)
        self.process_food_consumption()
        for callback in self.get_data_callbacks:
            callback()
        if self.current_time % Environment.FOOD_PARAMETERS['time'] == 0:
            self.add_some_food(Environment.FOOD_PARAMETERS['number_of_new_foods'])

    def add_data_callback(self, callback):
        self.get_data_callbacks += [callback]

    def skip_forward(self, iterations=100):
        for i in range(iterations):
            self.iterate()

    def add_some_food(self, food_to_add=5):
        self.foodage.add_random_foods(food_to_add)

    def add_some_organisms(self, organisms_to_add=5):
        self.organisms.add_random_blobs(number_of_new_blobs=organisms_to_add, current_time=self.current_time)
