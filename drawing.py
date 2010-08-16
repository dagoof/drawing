import re, os, sys, datetime, time, couchdb, uuid
from flask import Flask, jsonify, request, redirect, url_for, render_template, g, session, abort
from wtforms import Form, BooleanField, TextField, TextAreaField, IntegerField, FloatField, DecimalField, validators, ValidationError
from contextlib import closing
from functools import wraps


SECRET_KEY='devkey'
COUCH=couchdb.Server()
DEBUG=True

app=Flask(__name__)
app.config.from_object(__name__)

def init_db():
    dbs=['brush','palette','path']
    for db in dbs:
        if db in COUCH:
            COUCH.delete(db)
        COUCH.create(db)

@app.before_request
def before_request():
    g.Brush=COUCH['brush']
    g.Palette=COUCH['palette']
    g.Path=COUCH['path']

@app.after_request
def after_request(response):
    return response

@app.route('/')
def index():
    #print vars(request)
    sessionid=uuid.uuid4().hex
    return render_template('index.html', sessionid=sessionid)

@app.route('/api/post', methods=['GET','POST'])
def post():
    data=request.json
    session_id=data.get('session_id')
    coordinates=data.get('coordinates')
    brush=g.Brush.get(session_id, {'_id':session_id})
    tmp_coords=brush.get('coordinates', {})
    tmp_coords.update(coordinates)
    brush.update({'coordinates':tmp_coords})
    g.Brush.update([brush])
    return jsonify(status=True)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8096)
