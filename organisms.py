from blob import Blob


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
