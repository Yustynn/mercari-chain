'''Graph algorithm'''
import networkx

class ReputationGraph():
    def __init__(self):
        self.nodes = []
        self.edges = []

    def update(self):
        '''Recomputes graph weights'''
        # read all friendships and reviews in from db
        # compute with score algorithm
        pass

    def get_score_confidence(self, userid):
        '''Get the value of a given node'''
        score, confidence = 0, 0
        return (score, confidence)
