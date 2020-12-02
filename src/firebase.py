# firebase.py 
#
# this python file will handle user authentication: 
# user account creation, email verification triggers, traditional email sign-in, password reset 

from flask import flash, g, redirect, render_template, request, session, url_for, current_app, make_response, jsonify
from auth import create_jwt_token
import functools
import json
import requests
import pyrebase
import os
import jwt
import datetime

config = {
  "apiKey": os.getenv("FIREBASE_WEB_API_KEY"),
  "authDomain": os.getenv("AUTH_DOMAIN_FIREBASE"),
  "databaseURL": os.getenv("DATABASE_URL_FIREBASE"),
  "projectId": os.getenv("PROJECT_ID_FIREBASE"),
  "storageBucket": os.getenv("STORAGE_BUCKET_FIREBASE")
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

db = firebase.database()

def register():
    if request.method == 'POST':
        resp = None
        try:
            json_data = request.get_json()
            email = json_data.get('email')
            password = json_data.get('password')
            print(email, password)

            if not email:
                raise Exception('Email is required.')
            elif not password:
                raise Exception('Password is required.')
                    
            # verify email is not in use
            resp = auth.create_user_with_email_and_password(email, password)
            
            resp = clean_up_google_resp(resp)
                # TODO set user data in SQL DB
                # data = {
                #     "first_name": json_data['first_name'],
                #     "last_name": json_data['last_name'],
                #     "email": email
                # }
                # user = auth.sign_in_with_email_and_password(email, password)

                # TODO:  This should be done in SQL Database for User Info
                # db.child("users").child(user["localId"]).set(data)

        except requests.exceptions.HTTPError as e:
                error = json.loads(e.args[1])['error']['message']
                if error == "EMAIL_EXISTS":
                    return "Email already in use. Please Sign In.", 403
    
        except Exception as e:
            return str(e), 403

        else: 
            session.clear()
            session['user'] = resp

            return resp


def login():
    if request.method == 'POST':
        try:
            json_input = request.get_json()
            email = json_input["email"]
            password = json_input["password"]
            resp = auth.sign_in_with_email_and_password(email, password)
            resp = clean_up_google_resp(resp)
            
        except requests.exceptions.HTTPError as e:
            error = json.loads(e.args[1])['error']['message']
            return make_response(
                "Invalid Credentials: " + str(error),
                403,
                {"WWW-Authenticatie": "Basic relam: 'login needed' "}
            )
        
        except Exception as e:
            return make_response(
                "Unable to verify",
                403,
                {"WWW-Authenticatie": "Basic relam: 'login needed' "}
            )
        
        else:
            session.clear()
            session['user'] = resp
            session["logged_in"] = True

            token_for_user = create_jwt_token(email)
            resp["token"] = token_for_user.decode("utf-8")

            return make_response(resp)

def logout():
    session.clear()
    auth.current_user = None
    return jsonify("User Logged Out", 200)

def verifyEmail():
    # r is response object
    r = None 
    try:
        id_token = request.get_json().get("idToken")
        payload = json.dumps({
            "requestType": "VERIFY_EMAIL",
            "idToken": id_token
        })

        r = requests.post(os.getenv("GOOGLE_VERIFY_EMAIL_API"),
                        params={"key": os.getenv("FIREBASE_WEB_API_KEY")},
                        data=payload)
    except Exception as e:
        return make_response("Error In Verification Process" + str(e), 403)
    
    else:
        return r.json()


def clean_up_google_resp(resp: dict) -> dict:
    resp.pop("expiresIn")
    resp.pop("kind")
    more_account_info = auth.get_account_info(resp.get("idToken"))
    more_account_info = more_account_info.get("users")[0]
    more_account_info.pop("providerUserInfo")
    resp.update(more_account_info)
    return resp