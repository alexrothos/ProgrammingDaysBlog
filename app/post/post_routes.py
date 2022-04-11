from flask import request, jsonify

from flask_login import login_required

from app import app, db
from app.models import User, Post


@app.route('/post/', methods=['POST'])
@app.route('/post/<int:id>/', methods=['GET', 'PUT','DELETE'])
@app.route('/post/<string:username>/', methods=['GET'])
@login_required
def manage_post(post_id=None, username=None):
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
                if not post_id:
                    return jsonify({
                        'error': True,
                        'code': 400,
                        'title': 'Request failed',
                        'msg': 'Id is missing'
                    })
                post = Post.find_by_id(post_id)
                if not post:
                    return jsonify({
                        'error': True,
                        'code': 400,
                        'title': 'Request failed',
                        'msg': 'Post not found'
                    })
                post.title = title
                post.body = body
            try:
                post.save()
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
                post.delete_from_db()
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
        if post_id:
            post = Post.find_by_id(post_id)
            if not post:
                return jsonify({
                    'error': True,
                    'code': 400,
                    'title': 'Post not found',
                    'msg': 'Post not found'
                })
            return jsonify(post.serialize())
        elif username:
            user = User.find_by_name(username)
            if not user:
                return jsonify({
                    'error': True,
                    'code': 400,
                    'title': 'Request failed',
                    'msg': 'User not found'
                    }),400
            posts = Post.find_by_user_id(user_id)
            serialized_posts = [post.serialize() for post in posts]
            return jsonify(serialized_posts)
        else:
            return jsonify({
                'error': True,
                'code': 400,
                'title': 'Request failed',
                'msg': 'Post id or username is required'
                }),400

        # TODO find how to fetch user_id from login_required
        # TODO learn more about how to use marshmellow for making a model -> json