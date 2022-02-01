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
            title = data.get('title', None)
            body = data.get('body', None)
            if request.method == 'POST':
                user_id = data.get('user_id', None)
                post = Post(user_id=user_id,title=title, body=body)
            elif request.method == 'PUT':
                try:
                    post_id = data.get('id')
                    post = Post.find_by_id(post_id)
                except:
                    return jsonify({
                                    'error': True,
                                    'code': 400,
                                    'title': 'Request failed',
                                    'msg': 'Post not found or post id is missing'
                                    })
                post.title = title
                post.body = body
            try:
                db.session.add(post)
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
                'title': 'Post saved',
                'msg': 'Post saved'
            })
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
            data = request.get_json()
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

@app.route('/posts', methods=['GET'])
def posts():
    return jsonify(Post.all_posts())

@app.route('/user/<username>')
def user(username):
    try:
        return jsonify(User.find_user_by_name(username))
    except:
        return jsonify({
            "error": True,
            "code": 400,
            "title": "Request failed",
            "msg": "User not found"
        }), 400
