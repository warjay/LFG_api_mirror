import json
from math import ceil
import requests
from flask import jsonify # No need jsonify now actually, u can return dict directly and it will automatically jsonify it

def test():
    #Check if your api key is working
    with open('./LFG-api/secrets.txt') as f:
        secret = f.readline()
        print("Your secret:", secret)
        steamid = 76561197960434622 #some valve employee as per documentation
        url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + secret + "&steamid=" + steamid + "&format=json"
        response = requests.get(url)
        print("Working Secret:", response.status_code == 200)

def getSteamGames(steamid):
    with open('secrets.txt') as f:
        secret = f.readline()
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + secret + "&steamid=" + steamid + "&format=json&include_appinfo=true&include_played_free_games=true"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("API request failed")
    elif response.json()["response"] == {}:
        raise Exception("SteamID is private")
    else:
        jsonResponse = jsonify(response.json()["response"]["games"])
        #IMPORTANT STEP (HEADER), OR JAVASCRIPT CANNOT USE THIS DATA
        jsonResponse.headers['Access-Control-Allow-Origin'] = '*'
        return jsonResponse

def isValid(steamid):
    # Returns true if the steamid dosent throw error or is private  
    with open('./LFG-api/secrets.txt') as f:
        secret = f.readline()
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + secret + "&steamid=" + steamid + "&format=json"
    response = requests.get(url)
    return ((response.status_code == 200) and (response.json()["response"] != {}))

def getGameInfo(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&format=json"
    response = requests.get(url)
        
    if response.status_code != 200:
        raise Exception("API request failed")
    elif response.json()[str(appid)]["data"] == {}:
        raise Exception("Exception Thrown getGameInfo(), maybe appID is not valid?")
    else:
        jsonResponse = jsonify(response.json()[str(appid)]["data"])
        #IMPORTANT STEP (HEADER), OR JAVASCRIPT CANNOT USE THIS DATA
        jsonResponse.headers['Access-Control-Allow-Origin'] = '*'
        return jsonResponse

def getProfile(steamid):
    # Wait for tuan to implement
    # Vaguely following mockup + react
    # Get steam games can be another seperate call?
    ## yx- added username return because that would be much more convenient 🍿🦛
    print("SteamID: ",steamid)
    if steamid == "123": ##debug
        print("true")
        return()
    dictResponse = {
    "username": "LFG_USER",
    "aboutMe" : "It's all about the BOOM! Who's ready for story time with Adam Cole Bay Bay? Let me tell you why I betrayed MJF at Worlds' End... Lorem Ipsum dolor sit amet, test test test",
    "mostPlayedGame" : "Counter Strike 2",
    "mostPlayedGameHours" : 1000,
    "steamID": 12345678901234567,
    "friends" : [68696950647963075, 52052648627749864]
    }
    return(dictResponse)

def getSteamPicture(steamid):
    with open('./secrets.txt') as f:
        secret = f.readline().strip()
    
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={secret}&steamids={steamid}&format=json"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("API request failed")
    else:
        jsonResponse = jsonify(response.json()["response"]["players"][0]["avatarhash"])
        jsonResponse.headers['Access-Control-Allow-Origin'] = '*'
        return jsonResponse
    
def getMostPlayedGame(steamid):
    with open('secrets.txt') as f:
        secret = f.readline()
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={secret}&steamid={steamid}&format=json&include_appinfo=true&include_played_free_games=true"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("API request failed")
    else:
        data = response.json()
        if data["response"]["game_count"] == 0:
            return {"appid": None}

        highest_playtime = 0
        highest_playtime_appid = None
        gamename = ""

        for game in data['response']['games']:
            playtime_forever = game['playtime_forever']
            if playtime_forever > highest_playtime:
                highest_playtime = playtime_forever
                highest_playtime_appid = game['appid']
                gamename = game['name']

        highest_playtime = ceil(highest_playtime/60)

        return {
            "appid": highest_playtime_appid,
            "name": gamename,
            "hours": highest_playtime
        }




