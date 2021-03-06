from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify

from flask_login import current_user, login_required, login_user, logout_user

from app import app, db
from app.models import User, Post

@app.route('/')
def index():
    return "Server is running"

@app.route('/register/', methods=['POST'])
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
                user.save_to_db()
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

@app.route('/login/', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({
                    'error': False,
                    'code': 200,
                    'title': 'User is authenticated',
                    'msg': 'User is authenticated'
                }),200
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({
            'error': True,
            'code': 400,
            'title': 'Request failed',
            'msg': str(e)
            }), 400
    username = data.get("username", None)
    if not username:
        return jsonify({
            "error": True,
            "code": 400,
            "title": "Request failed",
            "msg": "Username not found"
            }), 400
    user = User.find_by_name(username)
    if not user:
        return jsonify({
            "error": True,
            "code": 400,
            "title": "Request failed",
            "msg": "User not found"
            }), 400
    if not check_password_hash(user.password_hash, data['password']):
        return jsonify({
            'error': True,
            'code': 400,
            'title': 'Invalid password',
            'msg': 'Password was wrong'
            }), 400
    else:
        login_user(user)
        return jsonify({
            'error': False,
            'code': 200,
            'title': 'Login in succesful',
            'msg': 'User is logged in'
            }), 200

@app.route('/logout/')
def logout():
    logout_user()
    return jsonify({
            'error': False,
            'code': 200,
            'title': 'Logout succesful',
            'msg': 'User is logged out'
            }), 200


@app.route('/user/<username>/', methods=['GET','PUT','DELETE'])
@app.route('/user/<int:id>/', methods=['GET','PUT','DELETE'])
def user_by_name(id=None,username=None):
    if username:
        user = User.find_by_name(username)
    elif id:
        user = User.find_by_id(id)
    if not user:
        return jsonify({
            "error": True,
            "code": 400,
            "title": "Request failed",
            "msg": "User not found"
        }), 400
    if request.method == 'GET':
        try:
            return jsonify(user.serialize())
        except Exception as e:
            return jsonify({
                "error": True,
                "code": 400,
                "title": "Error in JSON file",
                "msg": str(e)
            }), 400
    if request.method == 'DELETE':
        try:
            user.delete()
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
    if request.method == 'PUT':
        try:
            data = request.get_json()
        except Exception as e:
            return jsonify({
                'error': True,
                'code': 400,
                'title': 'Request failed',
                'msg': 'Bad request or lost data'
                }), 400
        user_id = data.get("id", None)
        user = User.find_by_id(user_id)
        if user:
            user.username = data.get('username')
            user.email = data.get('email')
            user.password = generate_password_hash(data.get('password'))
            try:
                user.save_to_db()
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
                'error': True,
                'code': 400,
                'title': 'User not found',
                'msg': 'User not found'
            }),200