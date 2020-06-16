from random import random
import numpy as np
import math
from quad_tree import Rectangle


class Blob:

    MASS_TO_RADIUS_SQUARED = 1000
    ENERGY_FOR_RADIUS_SQUARED_PRODUCTION = 1
    
    SPEED_EXTREMA = {
        "maximum": 0.08,
        "minimum": 0.0001
    }
    RADIUS_EXTREMA = {
        "maximum": 0.03,
        "minimum": 0.001
    }
    DEFAULT_STARTING_ENERGY_PER_RADIUS_SQUARED = 100

    ANGLE_PERTURBATION_RATE = 1

    MUTATION_PARAMETERS = {
        "speed": 0.1,
        "radius": 0.1,
        "starting_energy": 0.1
    }

    NUMBER_OF_BLOBS = 0

    def __init__(self, time_of_birth=0, angle=None, speed=None, position=None, energy=None, radius=None):

        self.time_of_birth = time_of_birth
        self.time_of_death = None

        self.id = Blob.NUMBER_OF_BLOBS
        Blob.NUMBER_OF_BLOBS += 1
        self.eye_width = 0.5*random() + 0.3
        if position is None:
            self.position = np.array(np.random.rand(2))
        else:
            self.position = position

        if angle is None:
            self.angle = random() * 2 * math.pi
        else:
            self.angle = angle

        if speed is None:
            self.speed = Blob.SPEED_EXTREMA["minimum"] + \
                         random() * (Blob.SPEED_EXTREMA["maximum"] - Blob.SPEED_EXTREMA["minimum"])
        else:
            self.speed = min(Blob.SPEED_EXTREMA["maximum"], max(speed, Blob.SPEED_EXTREMA["minimum"]))

        if radius is None:
            self.radius = Blob.RADIUS_EXTREMA["minimum"] + \
                          random() * (Blob.RADIUS_EXTREMA["maximum"] - Blob.RADIUS_EXTREMA["minimum"])
        else:
            self.radius = min(Blob.RADIUS_EXTREMA["maximum"], max(radius, Blob.RADIUS_EXTREMA["minimum"]))

        if energy is None:
            self.energy = Blob.DEFAULT_STARTING_ENERGY_PER_RADIUS_SQUARED * self.radius ** 2
        else:
            self.energy = energy
        self.starting_energy = self.energy

        self.bounding_box = self.make_bounding_box()
        self.next_offspring_data = self.make_next_offspring_data()

    def make_bounding_box(self):
        return Rectangle(
            x=self.position[0] - self.radius,
            y=self.position[1] - self.radius,
            width=2 * self.radius,
            height=2 * self.radius
        )

    def move_one_step(self):
        self.position += self.speed * self.get_velocity()
        self.position -= np.floor(self.position)
        self.bounding_box = self.make_bounding_box()

    def get_velocity(self):
        return self.speed * np.array([np.cos(self.angle), np.sin(self.angle)])

    def perturb_angle(self):
        self.angle += np.random.normal(0, Blob.ANGLE_PERTURBATION_RATE) * self.speed

    def change_energy(self, delta):
        self.energy += delta

    def eat_food(self, food):
        self.energy += food.energy

    def update(self, current_time: int):
        self.move_one_step()
        self.perturb_angle()
        self.change_energy(-0.5 * self.speed * self.speed * self.get_mass())
        if self.energy <= 0:
            self.time_of_death = current_time

    def produce_offspring(self, current_time: int):
        offspring = []
        while self.energy >= self.next_offspring_data["energy_requirement"] + self.starting_energy:
            offspring += [self.make_the_baby(current_time)]
            self.energy -= self.next_offspring_data["energy_requirement"]
            self.next_offspring_data = self.make_next_offspring_data()
        return offspring

    def get_capacity_for_birth(self):
        return self.energy / (self.next_offspring_data["energy_requirement"] + self.starting_energy)

    def is_dead(self):
        return not (self.time_of_death is None)

    def get_mass(self):
        return self.radius ** 2 * Blob.MASS_TO_RADIUS_SQUARED

    def get_energy(self):
        return self.energy

    def get_x_coordinate(self):
        return self.position[0]

    def get_y_coordinate(self):
        return self.position[1]

    def make_next_offspring_data(self):
        next_radius = max(
            np.random.normal(self.radius, Blob.MUTATION_PARAMETERS["radius"]*self.radius)
            , Blob.RADIUS_EXTREMA['minimum']
                        )
        next_starting_energy = max(np.random.normal(self.starting_energy,
                                                Blob.MUTATION_PARAMETERS["starting_energy"]*self.starting_energy),0)
        return {
            "speed": np.random.normal(self.speed, Blob.MUTATION_PARAMETERS["speed"]*self.speed),
            "radius": next_radius,
            "energy": next_starting_energy,
            "energy_requirement": Blob.reproduction_energy_requirement(next_starting_energy, next_radius)
        }

    @staticmethod
    def reproduction_energy_requirement(offspring_starting_energy, offspring_radius):
        return offspring_starting_energy + \
               Blob.ENERGY_FOR_RADIUS_SQUARED_PRODUCTION * offspring_radius ** 2

    def make_the_baby(self, birth_time):
        return Blob(
            time_of_birth=birth_time,
            speed=self.next_offspring_data["speed"],
            position=self.position.copy(),
            energy=self.next_offspring_data["energy"],
            radius=self.next_offspring_data["radius"]
        )

    def restrict_to_extrema(self):
        self.speed = min(Blob.SPEED_EXTREMA["maximum"], max(self.speed, Blob.SPEED_EXTREMA["minimum"]))
        self.radius = min(Blob.RADIUS_EXTREMA["maximum"], max(self.radius, Blob.RADIUS_EXTREMA["minimum"]))

    def __str__(self):
        return "<Blob #" + str(self.id) + ">"

    def left_eye_position(self):
        return self.position + self.radius/2 * np.array([np.cos(self.angle + self.eye_width), np.sin(self.angle + self.eye_width)])

    def right_eye_position(self):
        return self.position + self.radius/2 * np.array([np.cos(self.angle - self.eye_width), np.sin(self.angle - self.eye_width)])
