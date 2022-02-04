from flask import request, jsonify
from itsdangerous import json

from app import app, db
from app.models import User, Post

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
