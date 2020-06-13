from blob import Blob
from quad_tree import Rectangle, QuadTree


class Organisms:
    def __init__(self):
        self.organism_list = []
        self.organism_quad_tree = QuadTree(Rectangle(0, 0, 1, 1))

    def update(self, current_time):
        self.organism_quad_tree = QuadTree(Rectangle(0, 0, 1, 1))
        for blob in self.organism_list:
            blob.update(current_time)
            if blob.is_dead():
                self.kill_organism(blob, is_in_tree=False)
            else:
                for offspring in blob.produce_offspring(current_time):
                    self.add_blob(offspring)
                self.organism_quad_tree.insert(blob)

    def add_blob(self, blob):
        self.organism_list += [blob]
        self.organism_quad_tree.insert(blob)

    def add_random_blobs(self, number_of_new_blobs=1, current_time=0):
        for i in range(number_of_new_blobs):
            new_blob = Blob(time_of_birth=current_time)
            self.add_blob(new_blob)

    def kill_organism(self, organism, is_in_tree=True):
        self.organism_list.remove(organism)
        if is_in_tree:
            self.organism_quad_tree.remove(organism)

    def find_close_organisms(self, domain: Rectangle):
        close_organisms = []
        self.organism_quad_tree.retrieve_close_objects(domain, close_organisms)
        return close_organisms

    def update_extrema_of_organisms(self):
        for organism in self.organism_list:
            organism.restrict_to_extrema()
