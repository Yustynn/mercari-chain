'''Graph algorithm'''
from random import random
import networkx as nx
import numpy as np
import sqlite3

MAX_DEPTH = 4

class ReputationGraph():
    def __init__(self, conn, graph=nx.Graph()):
        self.conn = conn
        self.graph = graph

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
        scores_from_neighbors = (0, 0)
 
        if scores_tracker and confidences_tracker:
            scores_from_neighbors = (np.mean(scores_tracker), np.mean(confidences_tracker))
        own_scores = (core_scores[node], confidence_scores[node])

        
        def aggregate_score(own_score, neighbor_score, neighbor_factor):
            review_num = len(self.read_reviews((node,)))
            own_score
            return (1-np.exp(-review_num/10)) * own_score + (np.exp(-review_num/10)) * neighbor_score

        def aggregate_confidence(own_confidence, neighbor_confidence):
            review_num = len(self.read_reviews((node,)))
            return own_confidence + (1-own_confidence)*(np.exp(-review_num/10))*neighbor_confidence
            
        #print(own_scores)
        #print(scores_from_neighbors)
        vec = [score*confidence for score,confidence in zip(scores_tracker,confidences_tracker) if score != 0]
        #print(vec)
        neighbor_factor = np.mean(vec) if len(vec)!=0 else 0
        #print("awesome math function",neighbor_factor)
        comp_score = aggregate_score(own_scores[0],scores_from_neighbors[0],neighbor_factor)
        comp_conf = aggregate_confidence(own_scores[1],scores_from_neighbors[1])
        return (comp_score,comp_conf)

    def update(self):
        '''Recomputes graph weights'''
        user_ids, scores, confidences = self.read_users()
        for i in range(len(user_ids)):
            user_id = user_ids[i]
            core_score = scores[i]
            core_confidence = confidences[i]
            if user_id not in self.graph.nodes:
                self.graph.add_node(user_id, core_score=core_score, core_confidence=core_confidence)
            else:
                nx.set_node_attributes(self.graph,
                                       {user_id: {'core_score': core_score,
                                                  'core_confidence': core_confidence}})

        friendships = self.read_friendships()
        for edge in friendships:
            if not self.graph.has_edge(edge[0], edge[1]):
                self.graph.add_edge(edge[0], edge[1])

        for node in self.graph.nodes:
            #print("computing scores for node ", node)
            computed_score, computed_confidence = self.compute_scores(node)
            nx.set_node_attributes(self.graph,
                                   {node: {'computed_score': computed_score,
                                           'computed_confidence': computed_confidence}})

    def read_users(self):
        '''Return two lists of user id's and scores'''
        users, scores, confidences = [], [], []
        for user_id in self.conn.execute('SELECT UserId FROM USERS'):
            users.append(*user_id)
            reviews = self.read_reviews(user_id)
            score = 0
            if reviews:
                score = np.mean(reviews)
            scores.append(score)
            confidences.append(1-np.exp(-len(list(reviews))/60))
        return users, scores, confidences

    def read_reviews(self, user_id):
        cur = self.conn.execute("SELECT Rating FROM REVIEWS WHERE UserId=?",
                                         user_id)
        review_scores = [x[0] for x in cur.fetchall()]
        return review_scores

    def read_friendships(self):
        friendships = self.conn.execute("SELECT * FROM FRIENDS")
        return friendships

    def get_nodes(self):
        nodelist = []
        nodes = self.graph.nodes(data=True)
        for node in nodes:
            nodedict = {}
            nodedict['id'] = node[0]
            nodedict['trustworthiness'] = node[1]['core_score']
            nodedict['confidence'] = node[1]['core_confidence']
            nodedict['computed_score'] = node[1]['computed_score']
            nodedict['computed_confidence'] = node[1]['computed_confidence']
            nodelist.append(nodedict)
        return nodelist

    def get_edges(self):
        edgelist = []
        edges = self.graph.edges()
        for edge in edges:
            edgedict = {}
            edgedict['target'] = edge[0]
            edgedict['source'] = edge[1]
            edgelist.append(edgedict)
        return edgelist
