from flask import request, jsonify
from itsdangerous import json

from app import app, db
from app.models import User, Post

@app.route('/')
def index():
    return "Server is running"

@app.route('/post', methods=['GET','POST','PUT','DELETE'])
def manage_post():
    if request.method in ['POST', 'PUT']:
        # GET object supposed not to have a body.
        # The same with delete
        try:
            data = request.get_json()
        except Exception as e:
            return jsonify({
                'error': True,
                'code': 400,
                'title': 'Request failed',
                'msg': 'Bad request or lost data'
            })
        if data:
            # Gets field from body - title and body
            title = data.get('title', None)
            body = data.get('body', None)
            if request.method == 'POST':
                # If request is post creates a new object
                post = Post(title=title, body=body)
            elif request.method == 'PUT':
                # If request is put/patch updates an existing object
                # so you have to send an id in body
                # TODO return error response "request failed" when post not exist
                post_id = data.get('id')
                post_user_id = data.get('user_id')
                post = Post.find_by_id(post_id)
                post.title = title
                post.body = body
            try:
                # always try before commiting to database
                db.session.commit()
            except Exception as e:
                # whenever something gets wrong with save rollback (undo)
                db.session.rollback()
                return jsonify({
                    'error': True,
                    'code': 400,
                    'title': 'Request failed',
                    'msg': str(e)
                })
            return jsonify({
                'error': False,
                'code': 200,
                'title': 'Post saved',
                'msg': 'Post saved'
            })
        # No data means something broke with the request
        else:
            return jsonify({
                'error': True,
                'code': 400,
                'title': 'Request failed',
                'msg': 'Something went wrong. Please try again later'
            })
    # elif request.method == 'DELETE'
    # TODO add a delete method
    elif request.method == 'DELETE':
        try:
            id = data.get('id')
        except Exception as e:
            return jsonify({
                'error': True,
                'code': 400,
                'title': 'Request failed',
                'msg': 'Something went wrong, unable to delete the post'
            })
        # post_id find in DB
            # TODO how to find if the post_id is valid and then delete it...
        return "OK!"

    else: # request is GET
        # TODO find how to get a specific post with GET /post/{id}
        # TODO find how to fetch user_id from login_required
        posts = Post.find_by_user_id(User.id)
        # TODO learn more about how to use marshmellow for making a model -> json
        # TODO you have to return a list of posts in json

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        try:
            data = request.get_json()
        except Exception as e:
            return jsonify({
                'error': True,
                'code': 400,
                'title': 'Request failed',
                'msg': 'Bad request or lost data'
                })
        if data:
            username = data.get('name', None)
            email = data.get('email', None)
            user = User(username=username, email=email)
            user.set_password(data.get('password', None))
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    'error': True,
                    'code': 400,
                    'title': 'Request failed',
                    'msg': str(e)
                })
            return jsonify({
                'error': False,
                'code': 200,
                'title': 'User saved',
                'msg': 'User saved'
                })
        else:
            return jsonify({
                "error": True,
                "code": 400,
                "title": "Request failed",
                "msg": "Data are missing or lost"
            })
    else:
        return jsonify({
            "error": True,
            "code": 400,
            "title": "Request failed",
            "msg": "Error in request method"
        }) 

@app.route('/login', methods=['GET'])
def login():
    pass
 
