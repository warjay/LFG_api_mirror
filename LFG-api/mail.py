from mailjet_rest import Client

def sendResetMail(recipient, token):
    sender = "r87s82tij@mozmail.com"
    resetLink = "http://localhost:5173/resetPassword/" + token ##adding the final backslash blows up all the image directories... yeah -yx
    # limited to 200 emails per day
    # pretty much guaranteed to be in spam so look there first
    # due to security, i cant make reset address an anchor else gmail will remove the link
    api_key = '67cd703742e162fa6913edad859ca4cd'
    api_secret = 'b2c972f03e1c042bddbb34946ec139d1'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
        {
        "From": {
            "Email": sender,
            "Name": "CtrlCCtrlV"
        },
        "To": [
            {
            "Email": recipient,
            "Name": "You"
            }
        ],
        "Subject": "Reset Password",
        "TextPart": "Go to " + resetLink + " to reset your password. If you did not request a password reset, please ignore this email.",
        "HTMLPart": "<h3>Reset your password at "+ resetLink +"</h3><br /> If you did not request a password reset, please ignore this email."
        }
    ]
    }
    result = mailjet.send.create(data=data)
    # print(result.json())
    return result.status_code

