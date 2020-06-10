from organisms import Organisms
from foodage import Foodage
import numpy as np


class Environment:

    def __init__(self, number_of_blobs=0, starting_food_items=0):
        self.current_time = 0

        self.organisms = Organisms()
        self.organisms.add_random_blobs(number_of_blobs)

        self.foodage = Foodage()
        self.foodage.add_random_foods(starting_food_items)

        self.get_data_callbacks = []

    def process_food_consumption(self):
        for food in self.foodage.food_list:
            for organism in self.organisms.find_close_organisms(food.bounding_box):
                if organism.radius > food.radius and \
                        np.linalg.norm(food.position - organism.position) < organism.radius + food.radius:
                    organism.eat_food(food)
                    self.foodage.delete_food(food)
                    break

    def iterate(self):
        self.current_time += 1
        self.organisms.update()
        self.process_food_consumption()
        self.process_births()
        self.process_deaths()
        for callback in self.get_data_callbacks:
            callback()
        if self.current_time % 50 == 0:
            self.add_some_food(1)

    def add_data_callback(self, callback):
        self.get_data_callbacks += [callback]

    def process_births(self):
        for organism in self.organisms.organism_list:
            if organism.energy > 1:
                self.organisms.add_blob(organism.reproduce(birth_time=self.current_time))
                organism.change_energy(-0.5)

    def process_deaths(self):
        for organism in self.organisms.organism_list:
            if organism.energy < 0:
                self.organisms.kill_organism(organism)

    def skip_forward(self, iterations=100):
        for i in range(iterations):
            self.iterate()

    def restart(self):
        print("TODO: Restart")

    def add_some_food(self, food_to_add=5):
        self.foodage.add_random_foods(food_to_add)
