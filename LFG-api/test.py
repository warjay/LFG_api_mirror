#for anyone to test the log_in endpoint

import requests
import json

def testLogin():
    url = 'http://127.0.0.1:5000/api/log_in'

    # Define the JSON payload
    payload = {
        'username': 'user1',
        'password': 'password1'
    }

    # Convert the payload to JSON format
    json_payload = json.dumps(payload)

    # Set the headers
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the POST request
    response = requests.post(url, data=json_payload, headers=headers)

    # Print the response
    print(response.json())

def testRegister():
    url = 'http://127.0.0.1:5000/api/register'

    # Define the JSON payload
    payload = {
        'username': 'user1',
        'password': 'password1',
        'email': 'email1@email.com',
        'steamid' : 12345678901234567
    }

    # Convert the payload to JSON format
    json_payload = json.dumps(payload)

    # Set the headers
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the POST request
    response = requests.post(url, data=json_payload, headers=headers)

    # Print the response
    print(response.json())