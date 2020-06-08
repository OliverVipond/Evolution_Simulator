from blob import Blob
from quad_tree import Rectangle, QuadTree


class Organisms:
    def __init__(self, domain: Rectangle):
        self.organism_list = []
        self.organism_quad_tree = QuadTree(domain.copy())

    def update(self):
        self.organism_quad_tree.clear()
        for organism in self.organism_list:
            organism.update()
            self.organism_quad_tree.insert(organism)

    def add_blob(self, blob):
        self.organism_list += [blob]
        self.organism_quad_tree.insert(blob)

    def add_random_blobs(self, number_of_new_blobs=1):
        for i in range(number_of_new_blobs):
            new_blob = Blob()
            self.add_blob(new_blob)

    def kill_organism(self, organism):
        self.organism_list.remove(organism)

    def find_close_organisms(self, domain: Rectangle):
        return self.organism_quad_tree.retrieve(domain, [])
