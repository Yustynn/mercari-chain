'''Trust compuation server'''
from flask import Flask, request
from graph import ReputationGraph
import sqlite3

app = Flask(__name__)
graph = ReputationGraph()
conn = sqlite3.connect('example.db')

# POST methods
@app.route('/add_new_user/<int:user_id>')
def add_new_user(user_id):
    '''Add a new user to db and call graph.update'''
    friends = request.form['friends']
    pass

@app.route('/add_review/<int:user_id>')
def add_review(user_id):
    '''Add a new review to db and call graph.update'''
    rating = request.form['rating']
    content = request.form['content']
    #... this.update()
    pass

# GET methods
@app.route('/get/<int:fb_user_id>')
def get_score_confidence(fb_user_id):
    score, confidence = graph.get_score_confidence(fb_user_id)
    return score, confidence
