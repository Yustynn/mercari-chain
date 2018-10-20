'''Trust compuation server'''
from flask import Flask, request
from graph import ReputationGraph
from core_score import update_core_score_with_review
import sqlite3
import json

app = Flask(__name__)
graph = ReputationGraph()
conn = sqlite3.connect('projectxdb.db')


# POST methods
@app.route('/add_new_user/<int:user_id>', methods=['POST'])
def add_new_user(user_id):
    '''Add a new user to db and call graph.update'''
    print(user_id)
    name = request.form['name']
    friends = request.form['friends']
    add = conn.cursor()
    add.execute('''INSERT INTO USERS(UserId,Name) VALUES(?,?)''',
                (user_id, name))
    for friend in friends:
        add.execute('''INSERT INTO FRIENDS(UserId1,UserId2) VALUES(?,?)''',
                    (user_id, friend))

    graph.update()


@app.route('/add_review/<int:user_id>')
def add_review(user_id):
    '''Add a new review to db and call graph.update'''
    rating = request.form['rating']
    content = request.form['content']
    company = request.form['company']

    add = conn.cursor()
    add.execute('''INSERT INTO REVIEWS(UserId,Company,Rating,Content) VALUES(?,?,?,?)''',
                (user_id, company, rating, content))

    graph.update()


# GET methods
@app.route('/get/<int:fb_user_id>')
def get_score_confidence(fb_user_id):
    score, confidence = graph.get_score_confidence(fb_user_id)
    return json.dumps({"score": score, "confidence": confidence})


@app.route('/get/nodelist')
def get_nodelist():
    nodelist = graph.get_nodes()
    return json.dumps(nodelist)


@app.route('/get/edgelist')
def get_edgelist():
    edgelist = graph.get_edges()
    return json.dumps(edgelist)
