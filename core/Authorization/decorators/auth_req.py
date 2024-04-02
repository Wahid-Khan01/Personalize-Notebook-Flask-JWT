from functools import wraps
from flask import request, jsonify, session
import jwt
from core import x

def token_required(func):
    @wraps(func)
    def deco(*args, **kwargs):
        # token = request.headers.get('Authorization')
        token = request.cookies.get('token')
        if not token:
            return jsonify({'message': 'Token cookie is missing or invalid'}), 401
        token = token.replace('Bearer ', '')
        try:
            data = jwt.decode(token, x, algorithms=['HS256'])
            if session.get('uid') and session.get('uid') == data.get('uid'):
                return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'message': f'error: {e}'})
        
    return deco