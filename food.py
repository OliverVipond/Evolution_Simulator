from quad_tree import Rectangle
import numpy as np


class Food:
    def __init__(self, position=None, energy=None, radius=None):

        if position is None:
            self.position = np.array(np.random.rand(2))
        else:
            self.position = position

        if energy is None:
            self.energy = 0.5
        else:
            self.energy = energy

        if radius is None:
            self.radius = 0.01
        else:
            self.radius = radius

        self.bounding_box = Rectangle(x=self.position[0] - self.radius, y=self.position[1] - self.radius,
                                      width=2 * self.radius, height=2 * self.radius)

    # def update(self):
    #     print('update food')

    def get_x_coordinate(self):
        return self.position[0]

    def get_y_coordinate(self):
        return self.position[1]
