'''Trust compuation server'''
from flask import Flask, request
from graph import ReputationGraph
from core_score import update_core_score_with_review
import sqlite3
import json
import random

app = Flask(__name__)
conn = sqlite3.connect('projectxdb.db', check_same_thread=False)
graph = ReputationGraph(conn)


# POST methods
@app.route('/add_new_user/<int:user_id>', methods=['POST'])
def add_new_user(user_id):
    '''Add a new user to db and call graph.update'''
    name = request.form['name']
    add = conn.cursor()
    add.execute('''INSERT INTO USERS(UserId,Name) VALUES(?,?)''',
                (user_id, name))
    users = []
    for friend_id in conn.execute('SELECT UserId FROM USERS'):
        if random.random() < 0.3:
            add.execute('''INSERT INTO FRIENDS(UserId1,UserId2) VALUES(?,?)''',
                        (user_id, *friend_id))
    conn.commit()
    graph.update()
    return ''


@app.route('/add_review/<int:user_id>', methods=['POST'])
def add_review(user_id):
    '''Add a new review to db and call graph.update'''
    rating = request.form['rating']
    content = request.form['content']
    company = request.form['company']

    add = conn.cursor()
    add.execute('''INSERT INTO REVIEWS(UserId,Company,Rating,Content) VALUES(?,?,?,?)''',
                (user_id, company, rating, content))
    conn.commit()
    graph.update()
    return ''


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
