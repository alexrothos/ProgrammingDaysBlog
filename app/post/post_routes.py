from flask import request, jsonify
from itsdangerous import json

from app import app, db
from app.models import User, Post

from datetime import datetime


@app.route('/posts', methods=['GET'])
def posts():
    return jsonify(Post.all_posts())

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
                post.timestamp = datetime.utcnow()
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
            }),400
        if id:
            post_for_del = Post.find_by_id(id)
            try:
                db.session.delete(post_for_del)
            except:
                return jsonify({
                'error': True,
                'code': 400,
                'title': 'Request failed',
                'msg': 'Id not matching'
            }),400
        else:
            return jsonify({
                'error': True,
                'code': 400,
                'title': 'Request failed',
                'msg': 'Id was missing'
            }),400
        # post_id find in DB
            # TODO how to find if the post_id is valid and then delete it...

    else: # request is GET
        # TODO find how to get a specific post with GET /post/{id}
        # TODO find how to fetch user_id from login_required
        posts = Post.find_by_user_id(User.id)
        # TODO learn more about how to use marshmellow for making a model -> json
        # TODO you have to return a list of posts in json

@app.route('/post/<username>', methods=['GET'])
def post_by_user(username):
    posts = Post.find_by_user(username)
    return jsonify(posts)