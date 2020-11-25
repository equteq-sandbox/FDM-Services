import flask
import json
from service.UserService import *
from models.User import User

app = flask.Flask(__name__);

@app.route('/api/v1/user', methods=['POST'])
def addNewUser():
    params = flask.request.args
    addedUser = addUser(params); # add a user to db based on url params

    if addedUser:
        return flask.jsonify({"success": True}), 201

    return flask.abort(404)  


@app.route('/api/v1/user/<int:uid>', methods=['GET'])
def getUserById(uid):
    result = getUser(uid)
    if result:
        print(result.__dict__)
        return flask.jsonify(result.__dict__), 201
    return flask.abort(404)


if __name__ == "__main__":
    app.run()