from blob import Blob
from quad_tree import Rectangle, QuadTree


class Organisms:
    def __init__(self):
        self.organism_list = []
        self.organism_quad_tree = QuadTree(Rectangle(0, 0, 1, 1))

    def update(self):
        self.organism_quad_tree.clear()
        for organism in self.organism_list:
            organism.update()
            self.organism_quad_tree.insert(organism)

    def add_blob(self, blob):
        self.organism_list += [blob]
        self.organism_quad_tree.insert(blob)

    def add_random_blobs(self, number_of_new_blobs=1, current_time=0):
        for i in range(number_of_new_blobs):
            new_blob = Blob(time_of_birth=current_time)
            self.add_blob(new_blob)

    def kill_organism(self, organism):
        self.organism_list.remove(organism)
        self.organism_quad_tree.remove(organism)

    def find_close_organisms(self, domain: Rectangle):
        return self.organism_quad_tree.retrieve(domain, [])

    def update_bound_speed_of_organisms(self, minimum_speed, maximum_speed):
        Blob.change_speed_extrema(minimum=minimum_speed, maximum=maximum_speed)
        for organism in self.organism_list:
            organism.curb_speed()
