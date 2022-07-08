from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import flask
from flask import Flask, request, Response, jsonify, session, \
    render_template
import json
import requests
import uuid
from datetime import datetime

# Connect to our local MongoDB

client = MongoClient('mongodb://localhost:27017/')

# Choose DigitalNotes database

db = client['DigitalNotes']
usersColl = db['users']
notesColl = db['notes']

# Initiate Flask App

app = Flask(__name__)
app.secret_key = 'random'


# Common User functions

@app.route('/signup/', methods=['GET', 'POST'])
def signup():

    if usersColl.find_one({'username': request.args.get('username')}) \
        and usersColl.find_one({'email': request.args.get('mail')}):
        return 'done'
    else:
        user = {  
            '_id': str(uuid.uuid4()),
            # the fields that the user needs  to fill so as to sign up
            'email': request.args.get('mail'),
            'username': request.args.get('username'),
            'name': request.args.get('name'),
            'password': request.args.get('password'),
            'role': '1',
            }

        usersColl.insert_one(user)

        return (str(usersColl.find_one({'email': request.args.get('mail'
                )})), 200)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    user = usersColl.find_one({'username': request.args.get('username'
                              )})
    password = \
        usersColl.find_one({'password': request.args.get('password')})
    mail = usersColl.find_one({'email': request.args.get('mail')})

    if user and password and mail and password:

        role_tmp = \
            usersColl.find_one({'username': request.args.get('username'
                               ),
                               'password': request.args.get('password'
                               ), 'email': request.args.get('mail')},
                               {'_id': 0, 'role': 1})
        role_tmp = role_tmp['role']

        # if the role of the user is admin

        if role_tmp == '1':

            Id_tmp = \
                usersColl.find_one({'username': request.args.get('username'
                                   ),
                                   'password': request.args.get('password'
                                   ), 'email': request.args.get('mail'
                                   )}, {'_id': 1})
            session['role'] = role_tmp
            session['_id'] = Id_tmp['_id']
            return 'login succesfully'
        else:

        # if he is just a regular user

            Id_tmp = \
                usersColl.find_one({'username': request.args.get('username'
                                   ),
                                   'password': request.args.get('password'
                                   ), 'email': request.args.get('mail'
                                   )}, {'_id': 1})

            role_tmp = \
                usersColl.find_one({'username': request.args.get('username'
                                   ),
                                   'password': request.args.get('password'
                                   ), 'email': request.args.get('mail'
                                   )}, {'_id': 0, 'role': 1})

            session['role'] = role_tmp['role']
            session['_id'] = Id_tmp['_id']
            print (session['role'])
            return ('Login successfully', 200)
    else:
        session.pop('role', None)
        session.pop('_id', None)
        return ('Please try again something went wrong', 500)


@app.route('/createNote/', methods=['GET', 'POST'])
def CreateNote():
    now = datetime.now()
    if '_id' in session:

        Notes = {  # these are the fields that the user needs to fill so as to create a note
            'title': request.args.get('title'),
            'text': request.args.get('text'),
            'tags': request.args.get('tags'),
            '_id': str(uuid.uuid4()),
            'time': now.strftime('%H:%M:%S'),
            'user_Id': str(session['_id']),
            }

        notesColl.insert_one(Notes)

        return (str(notesColl.find_one({'user_Id': session['_id']})),
                200)
    else:
        # if the note already exists
        return ('Please try again something went wrong', 500)


@app.route('/title_Search/', methods=['GET', 'POST'])
def ttl_Search():

    if '_id' in session:

        return (str(notesColl.find_one({'title': request.args.get('title'
                ), 'user_Id': session['_id']})), 200)
    else:
        #there is no note with this title
        return ('Please try again something went wrong', 500)


@app.route('/tag_Search/', methods=['GET', 'POST'])
def tag_Search():

    if '_id' in session:

        return (str(notesColl.find_one({'tags': request.args.get('tags'
                ), 'user_Id': session['_id']})), 200)
    else:
        #there is no note with this tag
        return ('Please try again something went wrong', 500)


@app.route('/update/', methods=['GET', 'POST'])
def Update():
    #the user first types the title of the note that he wants to update
    #then the new fields are new_title , new_text , new_tags
    if '_id' in session:
        if notesColl.find_one({'title': request.args.get('title')}):
            if request.args.get('new_text'):
                new_text = request.args.get('new_text')
            else:
                txt = \
                    notesColl.find_one({'title': request.args.get('title'
                        )}, {'_id': 0, 'text': 1})
                new_text = txt['text']

            if request.args.get('new_tags'):

                new_tags = request.args.get('new_tags')
            else:
                tag = \
                    notesColl.find_one({'title': request.args.get('title'
                        )}, {'_id': 0, 'tags': 1})
                new_tags = tag['tags']

            if request.args.get('new_title'):
                new_title = request.args.get('new_title')
            else:
                tlt = \
                    notesColl.find_one({'title': request.args.get('title'
                        )}, {'_id': 0, 'title': 1})
                new_title = tlt['title']

            notesColl.update_many({'title': request.args.get('title')},
                                  {'$set': {'title': new_title,
                                  'text': new_text, 'tags': new_tags}})

            AllNotes = notesColl.find({})
            return flask.jsonify([notes for notes in AllNotes])
        else:
            #there is no note with this title to update
            return '0 Notes with this title please be sure that this specific note has been previously created '
    else:
        return ('Please try again something went wrong', 500)


@app.route('/delete_Note/', methods=['GET', 'POST'])
def delete_Note():
    # select the note you want to delete
    if '_id' in session:
        myquery = {'title': request.args.get('title'),
                   'user_Id': session['_id']}
        notesColl.delete_one(myquery)
        return str(notesColl.find_one({'title': request.args.get('title'
                   )}))
        
    else:
        #there is no note to delete with this title
        return ('Please try again something went wrong', 500)


@app.route('/sort/', methods=['GET', 'POST'])
def sort():
    # sort=+ or sort=-
    # ascending and descending view based on the date of the creation of the note
    if '_id' in session:
        sort = int(request.args.get('sort') + '1')
        AllNotes = notesColl.find().sort('time', sort)
        return flask.jsonify([notes for notes in AllNotes])
    else:
        return ('Please try again something went wrong', 500)


@app.route('/delete/', methods=['GET', 'POST'])
def delete():

    if '_id' in session:
        myquery = {'_id': session['_id']}
        usersColl.delete_one(myquery)
        return 'Deleted'
    else:
        return ('Please try again something went wrong', 500)


# Administrator functions

@app.route('/delete_Admin/', methods=['GET', 'POST'])
def delete_Admin():
    if '_id' and 'role' in session:
        if session['role'] == '0':
            return 'No permitted access'
        elif session['role'] == '1':
            if usersColl.find_one({'username': request.args.get('username'
                                  )}):
                myquery = {'username': request.args.get('username'),
                           'user_Id': session['_id']}
                usersColl.delete_one(myquery)

                return 'Deleted Administrator'
            else:
                return 'No user found be sure that the admin you are looking for has signed up'


@app.route('/Insert_Admin/', methods=['GET', 'POST'])
def Insert_Admin():
    if '_id' and 'role' in session:
        if session['role'] == '0':
            return 'No permitted access'
        elif session['role'] == '1':

            if usersColl.find_one({'username': request.args.get('username'
                                  )}) \
                and usersColl.find_one({'email': request.args.get('mail'
                    )}):#if the admin is already registered to the programm
                return 'User exists already try something else'
            else:
                user = { # the fields that the admin fills for the new admin
                    '_id': str(uuid.uuid4()),
                    'email': request.args.get('mail'),
                    'username': request.args.get('username'),
                    'name': request.args.get('name'),
                    'password': request.args.get('password'),
                    'role': '1',
                    }

                usersColl.insert_one(user)

                return (str(usersColl.find_one({'email': request.args.get('mail'
                        )})), 200)
    else:

        return ('Please try again something went wrong', 500)

# Flask App
# The programm is running on port 5000 at the localhost

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
