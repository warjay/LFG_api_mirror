# Get Data from Tuan DB
import requests
import json
# Endpoint
user_url = 'https://tuanisworkingonsomeproject.pythonanywhere.com/api/user/'

# Adds a user, no validation so be careful
def addUser(username, password, email, steamid):
    payload = {
        "username": username,
        "password_hash256": password,
        "email": email,
        "steamID": int(steamid)

    }
    json_payload = json.dumps(payload)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(user_url, data=json_payload, headers=headers)

    print(response.json())

def getUser(username):
    # Send GET request to retrieve user data
    response = requests.get(user_url, params={'all': False, 'username': username})
    if response.status_code == 404:
        return None
    return response.json()

def getAllUsers():
    # Send GET request to retrieve user data
    response = requests.get(user_url, params={'all': True})
    return response.json()

def updatePassword(username,password):
    print(username,password)
    data = getUser(username)
    data['password_hash256'] = password
    response = requests.put(user_url, params = {'username': username}, json = data)
    return response.status_code

def rateUser(username, rating):
    data = getUser(username)
    data["rating"] += rating
    response = requests.put(user_url, params = {'username': username}, json = data)
    return response.status_code