from flask import render_template,g,request
import json
import sqlite3
from app import app
import string
import pprint


DATABASE='dataset.sqlite'

def connect_to_database():
        return sqlite3.connect(DATABASE)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def root():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)
    return "HI"

    
@app.route("/hello")
def hello():
    print(url_for('static', filename='bob.html'))
    return "HI"

@app.route("/metric_explorer")
def metric_explorer():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('metric-explorer.html',
                           title='Home',
                           user=user)
    return "HI"

@app.route("/lookup")
def lookup():
    sub = request.args["term"]
    result=[{"desc":"234","id":"x"}, {"desc":"332", "id":"y"}]
    lst = string.split(sub,' ')
    newlst=[]
    for work in lst:
       x = work + "*"
       newlst.append( x)
    cursor = get_db().cursor()
    data = "".join(newlst)
    pprint.pprint(data)
    query = "select * from st3_metrics where title match ?"  ;
    result=cursor.execute(query, [data])
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append( dict([("desc",row[1]), ("id",row[0])]))

    print("-----------------------")
    pprint.pprint(result)
    #return jsonify(dict([("value","3"),("id","5")]))
    return json.dumps(result)


