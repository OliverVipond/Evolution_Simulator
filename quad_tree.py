from typing import List, Any


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


class Rectangle:
    def __init__(self, x, y, width, height):
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def rectangle_area(self):
        return self.height * self.width
