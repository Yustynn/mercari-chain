'''Graph algorithm'''
from random import random
import networkx as nx
import numpy as np
import sqlite3

MAX_DEPTH = 4

class ReputationGraph():
    def __init__(self, graph=nx.Graph()):
        self.graph = graph
        self.conn = sqlite3.connect('projectxdb.db')

    @staticmethod
    def random(N=50, p=0.1):
        def set_random_core_values(graph):
            core_scores = {node: random() for node in graph.nodes()}
            core_confidences = {node: random() for node in graph.nodes()}
            nx.set_node_attributes(graph, core_scores, 'core_score')
            nx.set_node_attributes(graph, core_confidences, 'core_confidence')

        graph = nx.fast_gnp_random_graph(N, p)
        set_random_core_values(graph)

        return ReputationGraph(graph)

    def compute_scores(self, node):
        scores_tracker = []
        confidences_tracker = []

        core_scores = nx.get_node_attributes(self.graph, 'core_score')
        confidence_scores = nx.get_node_attributes(self.graph, 'core_confidence')

        def populate_trackers(node, degree=None):
            if degree:
                scores_tracker.append(core_scores[node]**degree)
                confidences_tracker.append(confidence_scores[node]**degree)

                if degree is not MAX_DEPTH:
                    for node in self.graph.neighbors(node):
                        populate_trackers(node, degree + 1 if degree else 1)

        populate_trackers(node)

        scores_from_neighbors = (np.mean(scores_tracker), np.mean(confidences_tracker))
        own_scores = (core_scores[node], confidence_scores[node])

        def aggregate(own_score, neighbor_score):
            return 0.5 * own_score + 0.5 * neighbor_score

        return tuple(aggregate(*components) for components in zip(scores_from_neighbors, own_scores))

    def update(self):
        '''Recomputes graph weights'''
        user_ids, scores, confidences = self.read_users()
        for i in range(len(user_ids)):
            user_id = user_ids[i]
            core_score = scores[i]
            core_confidence = confidences[i]
            if user_id not in self.graph.nodes:
                self.graph.add_node(user_id, score=core_score, confidence=core_confidence)
            else:
                nx.set_node_attributes(self.graph,
                                       {user_id: {'core_score': core_score,
                                                  'core_confidence': core_confidence}})

        friendships = self.read_friendships()
        for edge in friendships:
            if not self.graph.has_edge(edge[0], edge[1]):
                self.graph.add_edge(edge[0], edge[1])

        for node in self.graph.nodes:
            computed_score, computed_confidence = self.compute_scores(node)
            nx.set_node_attributes(self.graph,
                                   {node: {'computed_score': computed_score,
                                           'computed_confidence': computed_confidence}})

    def read_users(self):
        '''Return two lists of user id's and scores'''
        users, scores, confidences = [], [], []
        for user_id in self.conn.execute('SELECT UserId FROM USERS'):
            users.append(user_id)
            reviews = self.read_reviews(user_id)
            scores.append(np.mean(reviews))
            confidences.append(1-np.exp(len(list(reviews))))
        return users, scores, confidences

    def read_reviews(self, user_id):
        review_scores = self.conn.execute("SELECT Rating FROM REVIEWS WHERE score=?",
                                         user_id)
        return review_scores

    def read_friendships(self):
        friendships = self.conn.execute("SELECT * FROM FRIENDSHIPS")
        return friendships

    def get_nodes(self):
        nodelist = []
        nodes = self.graph.nodes(data=True)
        for node in nodes:
            nodedict = {}
            nodedict['uid'] = node[0]
            nodedict['core_score'] = node[1]['core_score']
            nodedict['core_confidence'] = node[1]['core_confidence']
            nodedict['computed_score'] = node[1]['computed_score']
            nodedict['computed_confidence'] = node[1]['computed_confidence']
            nodelist.append(nodedict)
        return nodelist

    def get_edges(self):
        edgelist = []
        edges = self.graph.edges()
        for edge in edges:
            edgedict = {}
            edgedict['uid1'] = edge[0]
            edgedict['uid2'] = edge[1]
            edgelist.append(edgedict)
        return edgelist
