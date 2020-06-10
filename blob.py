from random import random
import numpy as np
import math
from quad_tree import Rectangle


class Blob:
    MAX_SPEED = 0.05
    MIN_SPEED = 0.000001

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
            self.speed = Blob.MIN_SPEED + random() * (Blob.MAX_SPEED - Blob.MIN_SPEED)
        else:
            self.speed = min(Blob.MAX_SPEED, max(speed, Blob.MIN_SPEED))

        if energy is None:
            self.energy = 0.5
        else:
            self.energy = energy

        if radius is None:
            self.radius = random() * 0.05
        else:
            self.radius = radius

        self.bounding_box = Rectangle(x=self.position[0] - self.radius, y=self.position[1] - self.radius,
                                      width=2 * self.radius, height=2 * self.radius)

    def update_position(self):
        self.position += self.speed * self.get_velocity()
        self.position -= np.floor(self.position)
        self.bounding_box = Rectangle(x=self.position[0] - self.radius, y=self.position[1] - self.radius,
                                      width=2 * self.radius, height=2 * self.radius)

    def get_velocity(self):
        return self.speed * np.array([np.cos(self.angle), np.sin(self.angle)])

    def perturb_angle(self):
        self.angle += np.random.normal(0, 0.1)

    def change_energy(self, delta):
        self.energy += delta

    def eat_food(self, food):
        self.energy += food.energy

    def update(self):
        self.update_position()
        self.perturb_angle()
        self.change_energy(-self.speed * self.speed * self.radius * self.radius * 500)

    def get_x_coordinate(self):
        return self.position[0]

    def get_y_coordinate(self):
        return self.position[1]

    def reproduce(self, birth_time):
        return Blob(time_of_birth=birth_time, speed=self.speed + np.random.normal(0, 0.003),
                    position=self.position.copy(),
                    energy=0.5,
                    radius=max(self.radius + np.random.normal(0, 0.001), 0.000001)
                    )

    def curb_speed(self):
        self.speed = min(Blob.MAX_SPEED, max(self.speed, Blob.MIN_SPEED))

    def __str__(self):
        return "<Blob #" + str(self.id) + ">"

    @staticmethod
    def change_speed_extrema(minimum, maximum):
        if maximum >= minimum >= 0:
            Blob.MAX_SPEED = maximum
            Blob.MIN_SPEED = minimum
        else:
            raise Exception("Maximum speed smaller than minimum speed")
