'''Graph algorithm'''
import networkx as nx
import sqlite3


class ReputationGraph():
    def __init__(self, graph=nx.Graph()):
        self.graph = graph
        self.conn = sqlite3.connect('db.db')

    def update(self):
        '''Recomputes graph weights'''
        users, scores = self.read_users()
        self.graph.add_nodes(users)
        # Assign scores to each node
        nx.set_node_attributes(self.graph, scores, 'core_score')
        # read all friendships and reviews in from db
        # compute with score algorithm
        pass

    def get_score_confidence(self, userid):
        '''Get the value of a given node'''
        score, confidence = 0, 0
        return (score, confidence)

    def read_users(self):
        '''Return two lists of user id's and scores'''
        users, scores = [], []
        for row in self.conn.execute('SELECT user_id, score FROM users'):
            user, score = row
            users.append(user)
            scores.append(score)
        return users, scores
