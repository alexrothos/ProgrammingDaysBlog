from flask import request, jsonify

from flask_login import login_required

from app import app, db
from app.models import User, Post

from datetime import datetime

@app.route('/post/', methods=['POST'])
@app.route('/post/<int:id>/', methods=['GET', 'PUT','DELETE'])
@app.route('/post/<string:username>/', methods=['GET'])
@login_required
def manage_post(id=None, username=None):
    if request.method in ['POST', 'PUT']:
        try:
            data = request.get_json()
        except Exception as e:
            return jsonify({
                'error': True,
                'code': 400,
                'title': 'Request failed',
                'msg': e
            })
        if data:
            title = data.get('title', None)
            body = data.get('body', None)
            if request.method == 'POST':
                user_id = data.get('user_id', None)
                post = Post(user_id=user_id,title=title, body=body)
            elif request.method == 'PUT':
                try:
                    post_id = id
                except:
                    return jsonify({
                                    'error': True,
                                    'code': 400,
                                    'title': 'Request failed',
                                    'msg': 'Id is missing'
                                    })
                post = Post.find_by_id(post_id)
                if post == None:
                    return jsonify({
                                    'error': True,
                                    'code': 400,
                                    'title': 'Request failed',
                                    'msg': 'Post not found'
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
    elif request.method == 'DELETE':
        if id:
            try:
                post = Post.query.filter_by(id=id).first()
                if not post:
                    return jsonify({
                        'error': True,
                        'code': 400,
                        'title': 'Request failed',
                        'msg': 'Post not found'
                        }),400
                db.session.delete(post)
                db.session.commit()
                return jsonify({
                        'error': False,
                        'code': 200,
                        'title': 'Post deleted',
                        'msg': 'Post deleted'
                        }),200
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    'error': True,
                    'code': 400,
                    'title': 'Request failed',
                    'msg': e
                    }),400
        else:
            return jsonify({
                'error': True,
                'code': 400,
                'title': 'Request failed',
                'msg': 'Id was missing'
            }),400
    else:
        if id is not None:
            post = Post.find_by_id(id)
            if post == None:
                    return jsonify({
                        'error': True,
                        'code': 400,
                        'title': 'Post not found',
                        'msg': 'Post not found'
                    })
            result = {
                    'id':post.id,
                    'user_id':post.user_id,
                    'title':post.title,
                    'body':post.body,
                    'timestamp':post.timestamp
                }
            return jsonify(result)
        elif username is not None:
            user_check = User.query.filter_by(username=username).first()
            if not user_check:
                return jsonify({
                    'error': True,
                    'code': 400,
                    'title': 'Request failed',
                    'msg': 'User not found'
                    }),400
            posts = Post.find_by_user(username)
            return jsonify(posts)
        else:
            return jsonify({
                'error': True,
                'code': 400,
                'title': 'Request failed',
                'msg': 'Post id or username is required'
                }),400

        # TODO find how to fetch user_id from login_required
        # TODO learn more about how to use marshmellow for making a model -> json