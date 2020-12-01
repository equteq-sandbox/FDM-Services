from flask import Flask, Response, jsonify, request, session, make_response
from flask_cors import cross_origin
from errors import AuthError
from functools import wraps
import datetime
import jwt
import os

app = Flask(__name__)
app.secret_key = os.getenv("FIRSTDAY_SECRETKEY")

def check_for_token(func):
    """ Declines access if the user doesn't have and provide the
    approrpiate the JSON Web Token. """

    @wraps(func)
    # Ensures we can wrap any function with any type of arguments
    def wrapped(*args, **kwargs):
        token = request.args.get("token")
        # if empty token, none was provided by user, is false
        if not token:
            return jsonify({"message": "Missing Token"}), 403
        else:
            try:
                jwt.decode(token, app.secret_key)
            except Exception as e:
                return jsonify({'Message': "Invalid Token, " + str(e)}), 403
            else:
                return func(*args, **kwargs)

    return wrapped

 
    
@app.route("/", methods=["GET"])
def health_endpoint():
	data = {"msg": "Hello World"}
	return jsonify(data)

@app.route("/public")
def public():
    return "Anyone can ping this endpoint"

@app.route("/private")
@check_for_token
def private():
    return "Only Viewable with a unexpired token is passed in"

@app.route("/auth/login", methods=["POST"])
def login():
    json_input = request.get_json()
    username = json_input["username"]
    password = json_input["password"]

    if username and password == "password":
        session["logged_in"] = True
        token_for_user = jwt.encode(
            {'user': username,
             'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
            },
            app.secret_key 
        )
        return jsonify({"token": token_for_user.decode("utf-8")})
    else:
        return make_response(
            "Unable to verify",
            403,
            {"WWW-Authenticatie": "Basic relam: 'login needed' "}
        )


if __name__ == "__main__":
    if os.getenv("env") == "localhost":
        app.run(debug=True)
    else:
        app.run()