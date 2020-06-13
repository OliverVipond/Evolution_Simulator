from typing import List, Any
from helpers import str_an_array


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


class QuadTree:
    nodes: List[Any]
    MAX_OBJECTS = 5
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

        self.nodes.append(QuadTree(Rectangle(x + sub_width, y + sub_height, sub_width, sub_height), self.level + 1))
        self.nodes.append(QuadTree(Rectangle(x, y + sub_height, sub_width, sub_height), self.level + 1))
        self.nodes.append(QuadTree(Rectangle(x, y, sub_width, sub_height), self.level + 1))
        self.nodes.append(QuadTree(Rectangle(x + sub_width, y, sub_width, sub_height), self.level + 1))

    def get_index(self, p_rect: Rectangle):
        index = -1
        if not self.has_nodes():
            return index

        vertical_midpoint = self.bounds.x + self.bounds.width / 2
        horizontal_midpoint = self.bounds.y + self.bounds.height / 2
        # bottom_quadrant = (p_rect.y < horizontal_midpoint and p_rect.y + p_rect.height < horizontal_midpoint)
        # top_quadrant = (p_rect.y > horizontal_midpoint)
        # TODO These functions should belong to Rectangle
        indices = []
        # Box is | 1 0 |
        #        | 2 3 |
        if p_rect.x <= vertical_midpoint and p_rect.y <= horizontal_midpoint:
            indices += [2]
        if p_rect.y + p_rect.height >= horizontal_midpoint and p_rect.x <= vertical_midpoint:
            indices += [1]
        if p_rect.x + p_rect.width >= vertical_midpoint and p_rect.y <= horizontal_midpoint:
            indices += [3]
        if p_rect.x + p_rect.width >= vertical_midpoint and p_rect.y + p_rect.height >= horizontal_midpoint:
            indices += [0]

        return indices

    def remove(self, object_to_remove):
        index = self.get_index(object_to_remove.bounding_box)
        if index != -1:
            self.nodes[index].remove(object_to_remove)
        else:
            self.objects.remove(object_to_remove)

    def insert(self, new_object):
        if self.has_nodes():
            indices = self.get_index(new_object.bounding_box)
            for index in indices:
                self.nodes[index].insert(new_object)
        else:
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
        while len(self.objects) > 0:
            indices = self.get_index(self.objects[0].bounding_box)
            for index in indices:
                self.nodes[index].insert(self.objects[0])
            self.objects.pop(0)

    def retrieve_close_objects(self, p_rect, close_objects):
        indices = self.get_index(p_rect)
        if self.has_nodes():
            for index in indices:
                self.nodes[index].retrieve_close_objects(p_rect, close_objects)
        else:
            close_objects += self.objects

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
