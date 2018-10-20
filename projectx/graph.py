'''Graph algorithm'''
from random import random
import networkx as nx
import numpy as np
import sqlite3

MAX_DEPTH = 4

class ReputationGraph():
    def __init__(self, graph=nx.Graph()):
        self.graph = graph
        self.conn = sqlite3.connect('db.db')

    @staticmethod
    def random(N = 50, p = 0.1):
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
