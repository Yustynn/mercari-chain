'''Trust compuation server'''
from flask import Flask
from graph import ReputationGraph
import sqlite3

app = Flask(__name__)
graph = ReputationGraph()

# POST methods
@app.route('/add_review/{user_id}')
def add_review():
    '''Add_review'''
    # Update graph

@app.route('/add_new_user')
def add_new_user(user_id, friends):
    '''Add a new user to db and call graph.update'''
    pass

def add_review(self, userid, rating):
    '''Add a new review to db and call graph.update'''
    #... this.update()
    pass

# GET methods
@app.route('')
def get_score_confidence(fb_user_id, platform):
    pass
