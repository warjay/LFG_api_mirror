# Backend Flask API  

## Requirements (Recommended in venv):  
pip install flask  
pip install flask python-dotenv  
pip install requests  
pip install Flask-JWT-Extended  
pip install flask_cors              (NEW!)  
pip install mailjet_rest            (NEW!)  

OR

pip install requirements.txt

## Steam Api key (Only needed for steam-api stuff, the get sessions dosent need it)
Get one from here, you need mobile guard: https://steamcommunity.com/dev/apikey  
Add key in secrets.txt file, it should look like this: 2006-SCSA-CtrlCCtrlV/LFG-api/secrets.txt  
It should NOT be uploaded when git pushing, entry has been added to gitignore  

## How to run:  
Open cmd in /LFG-api  
Enter in cmd: flask run  
Server runs at http://127.0.0.1:5000/  

## GET Data

#### getSteamGames
http://127.0.0.1:5000/api/getSteamGames/76561197960434622  
- You will get a json response of all the games userid 76561197960434622 owns, and the time played  
http://127.0.0.1:5000/api/getSteamGames/<userid>  
- replace <userid> with actual userid you want  

#### getSessions
http://127.0.0.1:5000/api/getSessions  
- Get json response of all sessions  
- currently only serves static data, which can be found at exampleGetSession.json

### getSteamPicture
http://127.0.0.1:5000/api/getSessions/76561197960434622
- You will get a json response of the avatar hash userid 76561197960434622 has

### getMostPlayedGame
http://127.0.0.1:5000/api/getMostPlayedGame/76561197960434622
- You will get a json response of {"appid": x} for userid 76561197960434622

#### getGameInfo
http://127.0.0.1:5000/api/getGameInfo/<appid>  
Returns game data json from steamapi  
Example: Returns data in: 730 > data from below link (too long to put here)  
https://store.steampowered.com/api/appdetails?appids=730&format=json  

#### getProfile
http://127.0.0.1:5000/api/getProfile/<steamid>  
- Currently returns a hardcoded profile (waiting for db)  
- if steamid == "123": returns nothing (for debugging)  
Current output:
~~~
{
    "username": "LFG_USER",
    "aboutMe" : "It's all about the BOOM! Who's ready for story time with Adam Cole Bay Bay? Let me tell you why I betrayed MJF at Worlds' End... Lorem Ipsum dolor sit amet, test test test",
    "mostPlayedGame" : "Counter Strike 2",
    "mostPlayedGameHours" : 1000,
    "steamID": 12345678901234567,
    "friends" : [68696950647963075, 52052648627749864]
}
~~~

## Login / Registration & Tokens
#### Login (api/log_in)
http://127.0.0.1:5000/api/log_in 
- Connected to tuan's db now
- Only accepts POST request  
- Returns json containing access token to create cookie on success, status code 200  
- Return json with error message and status code 401
- Can test using test.py or Postman
- Note: Will return status 500 (Internal Server Error) if username is blank

Sample body of POST:
~~~
{
    'username': 'user1',
    'password': 'password1'
}
~~~

Sample Errors:  
(User dosent exist)
~~~
{
    "error": "Invalid username"
}
~~~
(Password is empty or incorrect)
~~~
{
    "error": "Invalid password"
}
~~~
Sample output: 
~~~
{'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMDU4MTQyNCwianRpIjoiODk5YTg0MTItZWE5ZC00MWI3LWE1MTItZjlkODQwYzQ4NjgwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InVzZXIxIiwibmJmIjoxNzEwNTgxNDI0LCJjc3JmIjoiYTc1ZDRjN2UtNjU1MC00YzcyLTg5OWEtNTI5MWM0ODdhZTdkIiwiZXhwIjoxNzEwNTgyMzI0fQ.1rX52KWqwCeY8qnvkplcnQKtETzAfDKb8CY1BrKQRR0'}
~~~

#### Register (api/register)
http://127.0.0.1:5000/api/register
- Only accepts POST request  
- Returns json containing status code 400 and error messages for each invalid field
- If valid, returns status code 200 and success message
- Test using test.py or Postman

Sample body of POST:
~~~
{
    'username': 'user1',
    'password': 'password1',
    'email': 'email1@email.com',
    'steamid' : 12345678901234567
}
~~~

Error messages in response jsons:  
(If user alr exists)   
~~~
{"error": "Username already exists"}
~~~
(If email alr exists) (Waiting for DB)  
~~~
{"error": "Email already exists"}
~~~
(One for each error if username and email not duplicate)  
~~~
{
"username" : "Username must not be empty"  
"password" : "Password must be at least 8 characters long"  
"email" : "Invalid email"  
"steamid" : "Invalid Steam ID"
}  

~~~

## Forget/Reset Password  
### Forget Password (Send request to reset)
http://127.0.0.1:5000/api/forgetPassword/<email>
- CAPPED at 200 a day
- Look in SPAM folder, it will be there for sure
- Sends email with token

{"message": "Email sent"}, 200  
{"error": "Something went wrong"}, 400  

### Reset Password
Currently waiting on db  
WIP except for email sending  

## Authentication REQUIRED
- All in this field require JWT Header
- Postman users: Bearer Token option under auth, Token is the token u get from the login api
- Non-postman: Add {"Authorization": "Bearer TOKEN"} to header (replace TOKEN with actual token)

#### Rate User
http://127.0.0.1:5000/api/rateUser
- Rating is -1 / 0 / 1
- Rating of 0 does nothing
- Anything else will give error 400
- Username is target user, not sender
- Sender is gotten from token, so token from user1 will send rating from user1 (dosent care about which user sends currently since no logging)
- Does not log ratings currently, unless we implement on db (infinite ratings)

Example Payload :
~~~
{
    "username" : "user1"
    "rating" : -1
}
~~~

Responses:
~~~
{"message": "Rating successful"}, 200
{"error": "Username is problably wrong"}, 400
{"message": "Neutral rating sent"}, 200
{"error": "Invalid rating"}, 400
~~~