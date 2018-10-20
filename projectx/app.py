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
    print("test")
    print(user_id)
    print(request.form)
    name = request.form['name']
    print(name)
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
    resp = {"nodes": _get_nodelist(), "links": _get_edgelist()}
    return json.dumps(resp)

# POST methods
@app.route('/user', methods=['POST'])
def add_user():
    '''Add a new user to db and call graph.update'''
    user_num = len(graph.get_nodes())
    name = random.choice(["bob","alice","ken","donald","joe","yustynn","wim","bella"])
    add = conn.cursor()
    add.execute('''INSERT INTO USERS(UserId,Name) VALUES(?,?)''',
                (user_num, name))
    users = []
    for friend_id in conn.execute('SELECT UserId FROM USERS'):
        if random.random() < 0.3:
            add.execute('''INSERT INTO FRIENDS(UserId1,UserId2) VALUES(?,?)''',
                        (user_num, *friend_id))
    conn.commit()
    graph.update()
    resp = {"nodes": _get_nodelist(), "links": _get_edgelist()}
    return json.dumps(resp)


@app.route('/add_review/<int:user_id>', methods=['POST'])
def add_review(user_id):
    '''Add a new review to db and call graph.update'''
    count = request.form['count']
    rating = request.form['rating']
    content = request.form['content']
    company = request.form['company']

    add = conn.cursor()
    for i in range(int(count)):
        add.execute('''INSERT INTO REVIEWS(UserId,Company,Rating,Content) VALUES(?,?,?,?)''',
                    (user_id, company, rating, content))
    conn.commit()
    graph.update()
    resp = {"nodes": _get_nodelist(), "links": _get_edgelist()}
    return json.dumps(resp)


# GET methods
@app.route('/get/<int:fb_user_id>')
def get_score_confidence(fb_user_id):
    score, confidence = graph.get_score_confidence(fb_user_id)
    return json.dumps({"score": score, "confidence": confidence})


@app.route('/get/nodelist')
def get_nodelist():
    return json.dumps(_get_nodelist())


@app.route('/get/edgelist')
def get_edgelist():
    print("test")
    edgelist = graph.get_edges()
    return json.dumps(_get_edgelist())

def _get_nodelist():
    nodelist = graph.get_nodes()
    return nodelist

def _get_edgelist():
    edgelist = graph.get_edges()
    return edgelist
