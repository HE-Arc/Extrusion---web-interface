from flask_jwt_extended import get_jwt_claims
from functools import wraps


def mode_master(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            mode = get_jwt_claims()['mode']
            if mode == "master":
                return function(*args, **kwargs)
            raise KeyError
        except KeyError:
            return {'message': 'You are not authorized to access this route'}

    return wrapper


def mode_superuser(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            mode = get_jwt_claims()['mode']
            if mode == "superuser":
                return function(*args, **kwargs)
            raise KeyError
        except KeyError:
            return {'message': 'You are not authorized to access this route'}

    return wrapper


def mode_user(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            mode = get_jwt_claims()['mode']
            if mode == "master" or mode == "user":
                return function(*args, **kwargs)
            raise KeyError
        except KeyError:
            return {'message': 'You are not authorized to access this route'}

    return wrapper
