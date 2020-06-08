from typing import List, Any, Union

import numpy as np
from numpy.random import lognormal, gamma, uniform
from random import random
import math

import bokeh
from bokeh.models import ColumnDataSource, LinearColorMapper, ColorBar
from bokeh.plotting import ColumnDataSource, curdoc, Figure, show
from bokeh.driving import count
from bokeh.io import output_notebook
from bokeh.layouts import column, row

# Position: (x,y) \in [0,1]^2
# Velocity: [dx/dt, dy/dt]
# Energy: fraction of full energy 1
MAX_SPEED = 0.05


# --------------------------------------------------------------------------------#
#                                  QUAD TREE                                      #
# --------------------------------------------------------------------------------#

class Rectangle:
    def __init__(self, x, y, width, height):
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def rectangle_area(self):
        return self.height * self.width


class QuadTree:
    nodes: List[Any]
    MAX_OBJECTS = 10
    MAX_LEVELS = 5

    def __init__(self, p_level, p_bounds):
        self.level = p_level
        self.objects = []
        self.bounds = p_bounds
        self.nodes = []

    def clear(self):
        self.objects.clear()
        for i in range(len(self.nodes)):
            if self.nodes[i] is None:
                self.nodes[i].clear()
                self.nodes[i] = None

    def split(self):
        sub_width = self.bounds.width / 2
        sub_height = self.bounds.height / 2
        x = self.bounds.x
        y = self.bounds.y
        self.nodes = []

        self.nodes.append(QuadTree(self.level + 1, Rectangle(x + sub_width, y, sub_width, sub_height)))
        self.nodes.append(QuadTree(self.level + 1, Rectangle(x, y, sub_width, sub_height)))
        self.nodes.append(QuadTree(self.level + 1, Rectangle(x, y + sub_height, sub_width, sub_height)))
        self.nodes.append(QuadTree(self.level + 1, Rectangle(x + sub_width, y + sub_height, sub_width, sub_height)))

    def get_index(self, p_rect):
        index = -1
        vertical_midpoint = self.bounds.x + self.bounds.width / 2
        horizontal_midpoint = self.bounds.y + self.bounds.height / 2
        top_quadrant = (p_rect.y < horizontal_midpoint and p_rect.y + p_rect.height < horizontal_midpoint)
        bottom_quadrant = (p_rect.y > horizontal_midpoint)

        if p_rect.x < vertical_midpoint and p_rect.x + p_rect.width < vertical_midpoint:
            if top_quadrant:
                index = 1
            elif bottom_quadrant:
                index = 2

        elif p_rect.x > vertical_midpoint:
            if top_quadrant:
                index = 0
            elif bottom_quadrant:
                index = 3

        return index

    def insert(self, agent):
        if len(self.nodes) != 0:
            index = self.get_index(agent.bounding_box)
            if index != -1:
                self.nodes[index].insert(agent)
                return

        self.objects.append(agent)

        if len(self.objects) > QuadTree.MAX_OBJECTS and self.level < QuadTree.MAX_LEVELS:
            if len(self.nodes) == 0:
                self.split()
                i = 0
                while i < len(self.objects):
                    index = self.get_index(self.objects[i].bounding_box)
                    if index != -1:
                        self.nodes[index].insert(self.objects.pop(i))
                    else:
                        i += 1

    def retrieve(self, return_objects, p_rect):
        index = self.get_index(p_rect)
        if index != -1 and len(self.nodes) != 0:
            self.nodes[index].retrieve(return_objects, p_rect)

        return_objects += self.objects

        return return_objects


# --------------------------------------------------------------------------------#
#                                  CLASSES                                       #
# --------------------------------------------------------------------------------#

class Blob:
    def __init__(self, time_of_birth=0, angle=None, speed=None, position=None, energy=None, size=None):

        self.time_of_birth = time_of_birth

        if position is None:
            self.position = np.array(np.random.rand(2))
        else:
            self.position = position

        if angle is None:
            self.angle = random() * 2 * math.pi
        else:
            self.angle = angle

        if speed is None:
            self.speed = random() * MAX_SPEED
        else:
            self.speed = speed

        if energy is None:
            self.energy = 0.5
        else:
            self.energy = energy

        if size is None:
            self.size = random() * 0.05
        else:
            self.size = size

        self.bounding_box = Rectangle(x=self.position[0] - self.size, y=self.position[1] - self.size,
                                      width=2 * self.size, height=2 * self.size)

    def update_position(self):
        self.position += self.speed * self.get_velocity()
        self.position -= np.floor(self.position)
        self.bounding_box = Rectangle(x=self.position[0] - self.size, y=self.position[1] - self.size,
                                      width=2 * self.size, height=2 * self.size)

    def get_velocity(self):
        return self.speed * np.array([np.cos(self.angle), np.sin(self.angle)])

    def perturb_angle(self):
        self.angle += np.random.normal(0, 0.1)

    def update_energy(self, delta):
        self.energy += delta

    def eat_food(self, food):
        self.energy += food.energy

    def update(self):
        self.update_position()
        self.perturb_angle()
        self.update_energy(-self.speed * self.speed * self.size * self.size * 500)

    def get_x_coordinate(self):
        return self.position[0]

    def get_y_coordinate(self):
        return self.position[1]

    def reproduce(self, birth_time):
        return Blob(time_of_birth=birth_time, speed=max(self.speed + np.random.normal(0, 0.003), 0.000001),
                    position=self.position.copy(),
                    energy=0.5,
                    size=max(self.size + np.random.normal(0, 0.001), 0.000001)
                    )


class Food:
    def __init__(self, position=None, energy=None, size=None):

        if position is None:
            self.position = np.array(np.random.rand(2))
        else:
            self.position = position

        if energy is None:
            self.energy = 0.5
        else:
            self.energy = energy

        if size is None:
            self.size = 0.01
        else:
            self.size = size

        self.bounding_box = Rectangle(x=self.position[0] - self.size, y=self.position[1] - self.size,
                                      width=2 * self.size, height=2 * self.size)

    # def update(self):
    #     print('update food')

    def get_x_coordinate(self):
        return self.position[0]

    def get_y_coordinate(self):
        return self.position[1]


class Organisms:
    def __init__(self):

        self.organism_list = []

    def update(self):
        for organism in self.organism_list:
            organism.update()

    def add_blob(self, blob):
        self.organism_list += [blob]

    def add_random_blobs(self, number_of_new_blobs=1):
        for i in range(number_of_new_blobs):
            new_blob = Blob()
            self.add_blob(new_blob)

    def kill_organism(self, organism):
        self.organism_list.remove(organism)


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
            self.add_food(Food(energy=calories * calories, size=calories / 50))

    def delete_food(self, food):
        self.food_list.remove(food)


# --------------------------------------------------------------------------------#
#                                  DATA SOURCES                                  #
# --------------------------------------------------------------------------------#

blobs_source = ColumnDataSource(data=dict(x=[],
                                          y=[],
                                          size=[],
                                          alpha=[]
                                          )
                                )

food_source = ColumnDataSource(data=dict(x=[],
                                         y=[],
                                         size=[]
                                         )
                               )

stats = ColumnDataSource(data=dict(time=[],
                                   nbr_of_orgs=[],
                                   nbr_of_food=[]
                                   )
                         )

scatter = ColumnDataSource(data=dict(pop_sizes=[],
                                     pop_speeds=[],
                                     time_of_birth=[]
                                     )
                           )

reachable_org = ColumnDataSource(data=dict(x=[],
                                           y=[]
                                           )
                                 )
tracker = ColumnDataSource(data=dict(x=[],
                                     y=[]
                                     )
                           )

# --------------------------------------------------------------------------------#
#                                  FIGURE INIT                                   #
# --------------------------------------------------------------------------------#

scatter_plot = Figure(plot_width=400, plot_height=400)

env_plot = Figure(plot_width=600, plot_height=600, x_range=(0, 1), y_range=(0, 1))

stat_plot = Figure(plot_width=600, plot_height=200)

# --------------------------------------------------------------------------------#
#                                  SIM INIT                                      #
# --------------------------------------------------------------------------------#

organisms = Organisms()
organisms.add_random_blobs(10)

foodage = Foodage()
foodage.add_random_foods(30)

Organism_Tree = QuadTree(0, Rectangle(0, 0, 1, 1))

for org in organisms.organism_list:
    Organism_Tree.insert(org)


# --------------------------------------------------------------------------------#
#                                  UPDATE                                        #
# --------------------------------------------------------------------------------#

def make_org_data(organisms_class):
    return {
        'x': [organism.get_x_coordinate() for organism in organisms_class.organism_list],
        'y': [organism.get_y_coordinate() for organism in organisms_class.organism_list],
        'size': [organism.size for organism in organisms_class.organism_list],
        'alpha': [max(0, min(organism.energy, 1)) for organism in organisms_class.organism_list]
    }


def make_food_data(foodage_class):
    return {
        'x': [food.get_x_coordinate() for food in foodage_class.food_list],
        'y': [food.get_y_coordinate() for food in foodage_class.food_list],
        'size': [food.size for food in foodage_class.food_list]
    }


def consume_food(organism_quadtree, foodage_class):
    for food in foodage_class.food_list:
        close_orgs = organism_quadtree.retrieve([], food.bounding_box)
        for organism in close_orgs:
            if organism.size > food.size and \
                    np.linalg.norm(food.position - organism.position) < organism.size + food.size:
                organism.eat_food(food)
                foodage_class.delete_food(food)
                break


def kill_reproduce(organisms_class, t):
    for organism in organisms_class.organism_list:
        if organism.energy > 1:
            organisms_class.organism_list.append(organism.reproduce(birth_time=t))
            organism.update_energy(-0.5)
        if organism.energy < 0:
            organisms_class.kill_organism(organism)


blobs_source.stream(make_org_data(organisms))
food_source.stream(make_food_data(foodage))

env_plot.circle('x', 'y', radius='size', alpha='alpha', source=blobs_source, fill_color='green', line_color='black')
env_plot.circle('x', 'y', radius='size', alpha=1, source=food_source, fill_color='red', line_color='red')

env_plot.circle('x', 'y', alpha=1, size=4, source=reachable_org, fill_color='yellow', line_color='black')
env_plot.circle('x', 'y', alpha=1, size=4, source=tracker, fill_color='blue', line_color='blue')

stat_plot.line('time', 'nbr_of_orgs', source=stats, line_color='green')
stat_plot.line('time', 'nbr_of_food', source=stats, line_color='red')
stat_plot.x_range.follow = "end"
stat_plot.x_range.follow_interval = 100

color_mapper = LinearColorMapper(palette='Turbo256', low=0, high=1)
color_bar = ColorBar(color_mapper=color_mapper, location=(0, 0))

scatter_plot.circle('pop_sizes', 'pop_speeds', color={'field': 'time_of_birth', 'transform': color_mapper},
                    source=scatter)
scatter_plot.add_layout(color_bar, 'right')

curdoc().add_root(row(column(env_plot, stat_plot), scatter_plot))


@count()
def update(t):
    organisms.update()
    blobs_source.data = make_org_data(organisms)
    food_source.data = make_food_data(foodage)

    organism_tree = QuadTree(0, Rectangle(0, 0, 1, 1))

    for organism in organisms.organism_list:
        organism_tree.insert(organism)

    scatter.data = {
        'pop_sizes': [organism.size for organism in organisms.organism_list],
        'pop_speeds': [organism.speed for organism in organisms.organism_list],
        'time_of_birth': [organism.time_of_birth / (t + 1) for organism in organisms.organism_list]
    }

    consume_food(organism_tree, foodage)
    kill_reproduce(organisms, t)

    # tracked_food_item = foodage.food_list[0]
    #
    # tracker.data = {
    #     'x' : [tracked_food_item.get_x_coordinate()],
    #     'y' : [tracked_food_item.get_y_coordinate()],
    # }
    #
    #
    # reachable_org.data = {
    #     'x' : [org.get_x_coordinate() for org in Organism_Tree.retrieve([],tracked_food_item.bounding_box)],
    #     'y' : [org.get_y_coordinate() for org in Organism_Tree.retrieve([],tracked_food_item.bounding_box)],
    # }

    if t % 100 == 0:
        foodage.add_random_foods(1)
        stats.stream({
            'time': [t / 100],
            'nbr_of_orgs': [len(organisms.organism_list)],
            'nbr_of_food': [len(foodage.food_list)]
        })

        foodage.add_random_foods(1)


curdoc().add_periodic_callback(update, 10)
