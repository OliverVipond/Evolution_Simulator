from typing import List, Any
from helpers import str_an_array


class QuadTree:
    nodes: List[Any]
    MAX_OBJECTS = 10
    MAX_LEVELS = 5

    def __init__(self, p_bounds, p_level=1):
        self.level = p_level
        self.objects = []
        self.bounds = p_bounds
        self.nodes = []

    def clear(self):
        self.objects.clear()
        for i in range(len(self.nodes)):
            self.nodes[i].clear()
        self.nodes = []

    def create_nodes(self):
        sub_width = self.bounds.width / 2
        sub_height = self.bounds.height / 2
        x = self.bounds.x
        y = self.bounds.y
        self.nodes = []

        self.nodes.append(QuadTree(Rectangle(x + sub_width, y, sub_width, sub_height), self.level + 1))
        self.nodes.append(QuadTree(Rectangle(x, y, sub_width, sub_height), self.level + 1))
        self.nodes.append(QuadTree(Rectangle(x, y + sub_height, sub_width, sub_height), self.level + 1))
        self.nodes.append(QuadTree(Rectangle(x + sub_width, y + sub_height, sub_width, sub_height), self.level + 1))

    def get_index(self, p_rect):
        index = -1
        if not self.has_nodes():
            return index

        vertical_midpoint = self.bounds.x + self.bounds.width / 2
        horizontal_midpoint = self.bounds.y + self.bounds.height / 2
        top_quadrant = (p_rect.y < horizontal_midpoint and p_rect.y + p_rect.height < horizontal_midpoint)
        bottom_quadrant = (p_rect.y > horizontal_midpoint)
        # TODO These functions should belong to Rectangle

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

    def remove(self, object_to_remove):
        index = self.get_index(object_to_remove.bounding_box)
        if index != -1:
            self.nodes[index].remove(object_to_remove)
        else:
            self.objects.remove(object_to_remove)

    def insert(self, new_object):
        if self.has_nodes():
            index = self.get_index(new_object.bounding_box)
            if index != -1:
                self.nodes[index].insert(new_object)
                return

        self.objects.append(new_object)
        self.split_if_needed()

    def has_nodes(self):
        return len(self.nodes) != 0

    def split_if_needed(self):
        if len(self.objects) > QuadTree.MAX_OBJECTS \
                and self.level < QuadTree.MAX_LEVELS \
                and not self.has_nodes():

            self.create_nodes()
            self.move_objects_to_nodes()

    def move_objects_to_nodes(self):
        i = 0
        while i < len(self.objects):
            index = self.get_index(self.objects[i].bounding_box)
            if index != -1:
                self.nodes[index].insert(self.objects.pop(i))
            else:
                i += 1

    def retrieve(self, p_rect, return_objects):
        index = self.get_index(p_rect)
        if index != -1:
            self.nodes[index].retrieve(p_rect, return_objects)

        return_objects += self.objects

        return return_objects

    def __str__(self):
        if self.has_nodes():
            node_string = "; " \
               + str(self.nodes[0]) + "," \
               + self.nodes[1].__str__() + "," \
               + self.nodes[2].__str__() + "," \
               + self.nodes[3].__str__()
        else:
            node_string = ""
        return "{" + str_an_array(self.objects) + node_string + "}"


class Rectangle:
    def __init__(self, x, y, width, height):
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def rectangle_area(self):
        return self.height * self.width

    def copy(self):
        return Rectangle(self.x, self.y, self.width, self.height)
