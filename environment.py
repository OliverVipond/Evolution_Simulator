from organisms import Organisms
from foodage import Foodage
from quad_tree import Rectangle
import numpy as np


class Environment:
    def __init__(self, domain: Rectangle, number_of_blobs=0, starting_food_items=0):
        self.current_time = 0

        self.organisms = Organisms(domain)
        self.organisms.add_random_blobs(number_of_blobs)

        self.foodage = Foodage()
        self.foodage.add_random_foods(starting_food_items)

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

    def process_births(self):
        for organism in self.organisms.organism_list:
            if organism.energy > 1:
                self.organisms.add_blob(organism.reproduce(birth_time=self.current_time))
                organism.update_energy(-0.5)

    def process_deaths(self):
        for organism in self.organisms.organism_list:
            if organism.energy < 0:
                self.organisms.kill_organism(organism)
