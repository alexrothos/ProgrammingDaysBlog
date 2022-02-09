from datetime import datetime
from werkzeug.security import generate_password_hash
from flask import request, jsonify
from itsdangerous import json

from app import app, db
from app.models import User

@app.route('/')
def index():
    return "Server is running"

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
                }), 400
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
                }), 400
            return jsonify({
                'error': False,
                'code': 200,
                'title': 'User saved',
                'msg': 'User saved'
                }),200
        else:
            return jsonify({
                "error": True,
                "code": 400,
                "title": "Request failed",
                "msg": "Data are missing or lost"
            }), 400
    else:
        return jsonify({
            "error": True,
            "code": 400,
            "title": "Request failed",
            "msg": "Error in request method"
        }), 400

@app.route('/user_update', methods=['PUT'])
def user_update():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({
            'error': True,
            'code': 400,
            'title': 'Request failed',
            'msg': 'Bad request or lost data'
            }), 400
    try:
        username = data.get('username')
    except:
        return jsonify({
                'error':True,
                'code': 400,
                'title':'Request failed',
                'msg':'Username is missing'
            })
    user = User.query.filter_by(username=username).first()
    if user:
        user.email = data.get('email')
        user.password = generate_password_hash(data.get('password'))
        user.update_at = datetime.utcnow()
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
                }), 400
        return jsonify({
                'error': False,
                'code': 200,
                'title': 'User updated',
                'msg': 'User updated'
            }),200
    else:
        return jsonify({
                'error':True,
                'code': 400,
                'title':'Request failed',
                'msg':'User not found'
            })

@app.route('/user/by_name/<username>')
def user_by_name(username):
    user = User.find_user_by_name(username=username)
    if not user:
        return jsonify({
            "error": True,
            "code": 400,
            "title": "Request failed",
            "msg": "User not found"
        }), 400
    try:
        return jsonify(user)
    except Exception as e:
        return jsonify({
            "error": True,
            "code": 400,
            "title": "Wrong in JSON file",
            "msg": str(e)
        }), 400

@app.route('/user/by_id/<int:id>')
def user_by_id(id):
    user = User.find_user_by_id(id=id)
    if not user:
        return jsonify({
            "error": True,
            "code": 400,
            "title": "Request failed",
            "msg": "User not found"
        }), 400
    try:
        return jsonify(user)
    except Exception as e:
        return jsonify({
            "error": True,
            "code": 400,
            "title": "Wrong in JSON file",
            "msg": str(e)
        }), 400

@app.route('/user/delete/<username>', methods=['DELETE'])
def delete_user(username):
    user = User.find_user_by_name(username=username)
    if not user:
        return jsonify({
            "error": True,
            "code": 400,
            "title": "Request failed",
            "msg": "User not found"
        }), 400
    try:
        User.query.filter_by(username=username).delete()
        db.session.commit()
        return jsonify({
                'error': False,
                'code': 200,
                'title': 'User deleted',
                'msg': 'User deleted'
            }),200
    except Exception as e:
        db.session.rollback()
        return jsonify({
                    'error': True,
                    'code': 400,
                    'title': 'Request failed',
                    'msg': str(e)
                }), 400