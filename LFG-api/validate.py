

def validUsername(username):
    if username == "None" or username == "":
        return False
    return True

def validPassword(password):
    if password == "None" or password == "":
        return False
    if len(password) < 8:
        return False
    return True

def validEmail(email):
    if email == "None" or email == "":
        return False
    if email.count("@") != 1:
        return False
    if email.count(".") < 1:
        return False
    return True

def validSteamID(steamid):
    if steamid == "None" or steamid == "":
        return False
    if steamid.isdigit() == False:
        return False
    if len(steamid) != 17: # I think it has to be 17 digits?
        return False
    return True

def validateUser(username,password,email,steamid):
    response = dict()
    if not validUsername(username):
        response["username"] = "Username must not be empty"
    if not validPassword(password):
        response["password"] = "Password must be at least 8 characters long"
    if not validEmail(email):
        response["email"] = "Invalid email"
    if not validSteamID(steamid):
        response["steamid"] = "Invalid Steam ID"
    return response