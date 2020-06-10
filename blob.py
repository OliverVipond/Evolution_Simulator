from random import random
import numpy as np
import math
from quad_tree import Rectangle


class Blob:
    
    SPEED_EXTREMA = {
        "maximum": 0.05,
        "minimum": 0.000001
    }
    RADIUS_EXTREMA = {
        "maximum": 0.1,
        "minimum": 0.000001
    }

    ANGLE_PERTURBATION_RATE = 0.1

    MUTATION_PARAMETERS = {
        "speed": 0.003,
        "radius": 0.003
    }

    ENERGY_ON_BIRTH = 0.5

    MASS_TO_RADIUS_SQUARED = 1000

    NUMBER_OF_BLOBS = 0

    def __init__(self, time_of_birth=0, angle=None, speed=None, position=None, energy=None, radius=None):

        self.time_of_birth = time_of_birth

        self.id = Blob.NUMBER_OF_BLOBS
        Blob.NUMBER_OF_BLOBS += 1

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

        if energy is None:
            self.energy = Blob.ENERGY_ON_BIRTH
        else:
            self.energy = energy

        if radius is None:
            self.radius = Blob.RADIUS_EXTREMA["minimum"] + \
                          random() * (Blob.RADIUS_EXTREMA["maximum"] - Blob.RADIUS_EXTREMA["minimum"])
        else:
            self.radius = min(Blob.RADIUS_EXTREMA["maximum"], max(radius, Blob.RADIUS_EXTREMA["minimum"]))

        self.bounding_box = Rectangle(
            x=self.position[0] - self.radius,
            y=self.position[1] - self.radius,
            width=2 * self.radius,
            height=2 * self.radius
        )

    def update_position(self):
        self.position += self.speed * self.get_velocity()
        self.position -= np.floor(self.position)
        self.bounding_box = Rectangle(
            x=self.position[0] - self.radius,
            y=self.position[1] - self.radius,
            width=2 * self.radius,
            height=2 * self.radius
        )

    def get_velocity(self):
        return self.speed * np.array([np.cos(self.angle), np.sin(self.angle)])

    def perturb_angle(self):
        self.angle += np.random.normal(0, Blob.ANGLE_PERTURBATION_RATE)

    def change_energy(self, delta):
        self.energy += delta

    def eat_food(self, food):
        self.energy += food.energy

    def update(self):
        self.update_position()
        self.perturb_angle()
        self.change_energy(-0.5 * self.speed * self.speed * self.get_mass())

    def get_mass(self):
        return self.radius * self.radius * Blob.MASS_TO_RADIUS_SQUARED

    def get_x_coordinate(self):
        return self.position[0]

    def get_y_coordinate(self):
        return self.position[1]

    def reproduce(self, birth_time):
        return Blob(
            time_of_birth=birth_time,
            speed=self.speed + np.random.normal(0, Blob.MUTATION_PARAMETERS["speed"]),
            position=self.position.copy(),
            energy=Blob.ENERGY_ON_BIRTH,
            radius=self.radius + np.random.normal(0, Blob.MUTATION_PARAMETERS["radius"])
        )

    def restrict_to_extrema(self):
        self.speed = min(Blob.SPEED_EXTREMA["maximum"], max(self.speed, Blob.SPEED_EXTREMA["minimum"]))
        self.radius = min(Blob.RADIUS_EXTREMA["maximum"], max(self.radius, Blob.RADIUS_EXTREMA["minimum"]))

    def __str__(self):
        return "<Blob #" + str(self.id) + ">"

    @staticmethod
    def change_speed_extrema(minimum, maximum):
        if maximum >= minimum >= 0:
            Blob.SPEED_EXTREMA["maximum"] = maximum
            Blob.SPEED_EXTREMA["minimum"] = minimum
        else:
            raise Exception("Maximum speed smaller than minimum speed")
