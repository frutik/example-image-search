from annoy import AnnoyIndex


class SearchIndex(object):
    def __init__(self):
        self.annoy = AnnoyIndex(512, 'angular')

    def load(self, index_file):
        self.annoy.load(index_file)

    def find_similar(self, vector, num=5):
        self.annoy.get_nns_by_vector(vector, num)
