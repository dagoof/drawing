import re, os, sys, datetime, time, couchdb, uuid, json
from flask import Flask, jsonify, request, redirect, url_for, render_template,\
    g, session, abort
from wtforms import Form, BooleanField, TextField, TextAreaField, IntegerField,\
    FloatField, DecimalField, validators, ValidationError
from setlogic import dict_insert, dict_remove, dict_remove_from_paths
from contextlib import closing
from functools import wraps


SECRET_KEY='devkey'
COUCH=couchdb.Server()
DEBUG=True
REPO_DIR='repos'

app=Flask(__name__)
app.config.from_object(__name__)

def init_db():
    dbs=['brush','palette','path','revision']
    for db in dbs:
        if db in COUCH:
            COUCH.delete(db)
        COUCH.create(db)

@app.before_request
def before_request():
    g.Brush=COUCH['brush']
    g.Palette=COUCH['palette']
    g.Path=COUCH['path']
    g.Revision=COUCH['revision']
    g.dbs={'brush': g.Brush, 'palette': g.Palette, 'path': g.Path}

@app.after_request
def after_request(response):
    return response

@app.route('/')
def index():
    #print vars(request)
    sessionid=uuid.uuid4().hex
    os.mkdir(os.path.join(REPO_DIR, sessionid))
    return render_template('index.html', sessionid=sessionid)

@app.route('/api/post', methods=['POST'])
def post():
    data=request.json
    session_id=data.get('session_id')
    coordinates=data.get('coordinates')
    uid=uuid.uuid1().hex
    brush=g.Brush.get(session_id, {'_id':session_id})
    tmp_coords=brush.get('coordinates', {})
    tmp_coords.update(coordinates)
    brush.update({'coordinates':tmp_coords})
    g.Brush.update([brush])
    return jsonify(status=True)

@app.route('/api/commit', methods=['POST'])
def commit():
    data=request.json
    uid=uuid.uuid1().hex
    session_id, _last_commit=(data.get(x) for x in ('session_id', 'last_commit'))
    document_data=data.get('data', {})
    commit={'_id': uid, 'meta': 
            {'session_id': session_id, '_last_commit': _last_commit,
                '_timestamp': time.time()}}
    for name, db in g.dbs.items():
        if name in document_data:
            this_data=document_data.get(name)
            current=db.get(session_id, {'_id': session_id})
            dict_insert(current, this_data)
            commit_data={name: {'_id': session_id, 'added': this_data, 'removed': {}}}
            dict_insert(commit, commit_data)
            db.update([current])

    g.Revision.update([commit])
    return jsonify({'status':True})


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8096)
