# auth.py
#
# This module holds unused advanced function prototypes that
# handle JWTs tokens and HTTP Authorization headers

from errors import AuthError
from flask import Flask, Response, jsonify, request, session, make_response, g, current_app
import functools
import jwt
import datetime

def login_required(view):
    # Wrapper function to check if user is logged in.
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify("User Not Logged In", 403)
        return view(**kwargs)

    return wrapped_view

def check_for_token(func):
    """ Declines access if the user doesn't have and provide the
    approrpiate the JSON Web Token. """

    @functools.wraps(func)
    # Ensures we can wrap any function with any type of arguments
    def wrapped(*args, **kwargs):
        try:
            json_body_input = request.get_json()
            token = json_body_input.get("token")
            jwt.decode(token, current_app.secret_key)

        except AttributeError:
            return jsonify({"message": "Missing Token"}), 403

        except Exception:
            # this catch includes all raised errors
            # even jwt.exceptions.InvalidSignatureError
            return jsonify({'Message': "Invalid Token"}), 403
        
        else:
            return func(*args, **kwargs)

    return wrapped

def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    # token = get_token_auth_header()
    # unverified_claims = jwt.get_unverified_claims(token)
    # if unverified_claims.get("scp"):
    #     token_scopes = unverified_claims["scp"].split()
    #     for token_scope in token_scopes:
    #         if token_scope == required_scope:
    #             return True
    return False


def get_token_auth_header():
    """ Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                         "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Authorization header must start with"
                         " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Authorization header must be"
                         " Bearer token"}, 401)

    token = parts[1]
    return token

def create_jwt_token(email: str):
    return  jwt.encode({'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        },
        current_app.secret_key)