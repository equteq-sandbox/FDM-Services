# auth.py
#
# This module holds unused advanced function prototypes that
# handle JWTs tokens and HTTP Authorization headers

from errors import AuthError
from flask import Flask, Response, jsonify, request, session, make_response
from functools import wraps
import jwt


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