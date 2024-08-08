import os
from flask import Flask, send_from_directory, Response, request
import steamapi
import json
import validate
import tuan
import mail
import datetime
# Authentication
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder='../LFG-app')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Flask-JWT-Extended Setup
app.config["JWT_SECRET_KEY"] = "itsProblablyFineToUploadThisToGithub"
jwt = JWTManager(app)

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    print("Why are you routing to main?")
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


# Debug Endpoints
@app.route('/api/getToken/username')
def getToken(username):
    access_token = create_access_token(identity=username)
    return {"access_token": access_token}, 200



# eg http://127.0.0.1:5000/api/log_in/
# Login
@app.route('/api/log_in', methods = ['POST']) # Note endpoint is log_in as login dosent work for some arcane reason
def login():
    user = tuan.getUser(request.json.get("username"))
    if user is None:
        # If none means user does not exist
        return {"error": "Invalid username"}, 401
    if user['password_hash256'] != request.json.get("password"):
        return {"error": "Invalid password"}, 401
    else:
        expires = datetime.timedelta(minutes=5)
        access_token = create_access_token(identity=request.json.get("username"),expires_delta=expires)
        # Return access token for client side to generate cookie for header
        return {"access_token": access_token}, 200






# API Endpoints

#eg http://127.0.0.1:5000/api/getSteamGames/76561197960434622
@app.route('/api/getSteamGames/<steamid>')
def getSteamGames(steamid):
    return steamapi.getSteamGames(steamid)

@app.route('/api/getSteamPicture/<steamid>')
def getSteamPicture(steamid):
    return steamapi.getSteamPicture(steamid)

@app.route('/api/getMostPlayedGame/<steamid>')
def getMostPlayedGames(steamid):
    return steamapi.getMostPlayedGame(steamid)

#get sessions for testing
@app.route('/api/getSessions')
def getSessions():
    with open('exampleGetSession.json') as file:
        data = json.load(file)

    # Convert the data to JSON string
    response_data = json.dumps(data)
    # Create a response with the JSON data
    response = Response(response_data, content_type='application/json')
    # Add the 'Access-Control-Allow-Origin' header
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response

#get game info
@app.route('/api/getGameInfo/<appid>')
def getGameInfo(appid):
    print(steamapi.getGameInfo(appid))
    return steamapi.getGameInfo(appid)

@app.route('/api/getProfile/<steamid>')
def getProfile(steamid):
    return steamapi.getProfile(steamid) 

@app.route('/api/register', methods=['POST'])
def register():
    json_data = request.get_json()
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")
    steamid = request.json.get("steamid")
    if tuan.getUser(username) is not None:
        return {"error": "Username already exists"}, 400
    
    # TODO: Waiting for db to be updated
    # if tuan.getUserByEmail(email) is not None:
    #     return {"error": "Email already exists"}, 400

    response = validate.validateUser(username,password,email,steamid)
    if response:
        # Returns which part is wrong, can be multiple
        return response, 400
    else:
        # No error msg, so send success and add user to db
        tuan.addUser(username,password,email,steamid)
        return {"message": "Registration successful"}, 200

@app.route('/api/forgetPassword/<email>')
def forgetPassword(email):
    # Send email capped at 200 a day so please dont spam
    expires = datetime.timedelta(minutes=5)
    token = create_access_token(identity=email,expires_delta=expires) # misusing the token system for now
    if mail.sendResetMail(email,token) == 200:
        return {"message": "Email sent"}, 200
    else:
        return {"error": "Something went wrong"}, 400
    
@app.route('/api/debugGenerateToken/<email>')
def debugGenerateToken(email):
    # Send email capped at 200 a day so please dont spam
    token = create_access_token(identity=email) # misusing the token system for now
    return {"token": token}, 200

    
@app.route('/api/resetPassword', methods=['POST'])
def resetPassword():
    print(request)
    # Username for now until db is updated
    username = request.json.get("username")
    password = request.json.get("password")
    tuan.updatePassword(username,password)
    
    return {"message": "Password updated"}, 200

@cross_origin(supports_credentials=True, methods=["GET, POST, OPTIONS"], headers=["content-type, auth"])
@app.route('/api/authEmailToken', methods=['GET'])
@jwt_required()
def authEmailToken():
    email = get_jwt_identity() ## get email back from token
    print(email)
    

    ##### BIG BIG BIG PLACEHOLDER ---- SUPPOSED TO FIND THE USER THAT THE EMAIL BELONGS TO!
    ###lets pretend it does ya
    return({"email":email}), 200 ##returning the email because i'm having to do this big big workaround -yx
    ##### PLACEHOLDER


# Requires JWT (need use token from login as header)
# Send rating and username to rate as payload
# See readme to see how to set header
@app.route('/api/rateUser', methods=['POST'])
@jwt_required()
def rateUser():
    # This dosent actually do anything with the user that is rating currently, just the target
    rating = request.json.get("rating") # -1 / 0 / 1
    username = request.json.get("username")
    if rating == 1 or rating == -1:
        if tuan.rateUser(username,rating) == 200:
            return {"message": "Rating successful"}, 200
        else:
            return {"error": "Username is problably wrong"}, 400
    if rating == 0: # Neutral rating or user dosent want to rate
        return {"message": "Neutral rating sent"}, 200
    else:
        return {"error": "Invalid rating"}, 400
        