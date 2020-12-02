from flask import Flask, Response, jsonify, request, session, make_response, g, redirect, url_for
from flask_cors import cross_origin
from errors import AuthError
from auth import check_for_token, login_required
import functools
import datetime
import firebase
import jwt
import os

app = Flask(__name__)
app.secret_key = os.getenv("FIRSTDAY_SECRETKEY")


@app.route("/public")
def public():
    return "Anyone can ping this endpoint"


@app.route("/private")
@check_for_token
def private():
    return "Only Viewable with a unexpired token is passed in"


@app.route('/auth/register', methods=['POST'])
def register():
    return jsonify(firebase.register())


@app.route('/auth/verifyEmail', methods=['POST'])
def verifyEmail():
    return firebase.verifyEmail()


@app.route('/auth/login', methods=['POST'])
def firebase_login():
    return firebase.login()


@app.route('/auth/logout', methods=['GET'])
@login_required
def firebase_logout():
    return firebase.logout()


@app.before_request
# this gets executed before ANY request.
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user = session.get("user")

    try:
        name = session.get('name')['first_name']
    except:
        name = None

    if user is None:
        g.user = None
        g.name = None
    else:
        g.user = user
        g.name = name


if __name__ == "__main__":
    if os.getenv("env") == "localhost":
        app.run(debug=True)
    else:
        app.run()