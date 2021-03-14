from constants import API_BASE_URL, HEADER_X_APP_ID, HEADER_X_APP_KEY, HEADER_X_DEVICE_ID, HEADER_X_DEVICE_PLATFORM, \
    HEADER_X_DEVICE_TYPE, HEADER_X_API_KEY
import requests
import json

url = API_BASE_URL + "rest-api/pub/api/v2/login/ott"
header_app_id = "ott-app"
header_app_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6ImR2ci11aSIsImtleSI6IiJ9.XUQUYRo82fD_6yZ9ZEWcJkc0Os1IKbpzynLzSRtQJ-E"
header_api_key = "9a8087f911b248c7945b926f254c833b"
platform_android = "Android"
app_version = "11.0"
fallback_rmn = ""
user = {}


def generateOTP(sid, rmn):
    if sid == "":
        print("Generating OTP with Registered Mobile Number...", rmn)
        otp_with_rmn_url = API_BASE_URL + "rest-api/pub/api/v1/rmn/" + rmn + "/otp"
        x = requests.get(otp_with_rmn_url)
        if x.status_code == 200:
            msg = x.json()['message']
            if msg == 'OTP generated successfully.':
                print("OTP Generated successfully")
            else:
                print(msg)

        else:
            print("Failed to generate OTP")

    else:
        print("Generating OTP with Subscriber ID..", sid)
        otp_with_sid_url = API_BASE_URL + "rest-api/pub/api/v1/subscribers/" + sid + "/otp"
        x = requests.get(otp_with_sid_url)

        if x.status_code == 200:
            msg = x.json()['message']
            if msg == 'OTP generated successfully.':
                fallback_rmn = str(x.json()['data']['rmn'])
                print("Rmn:", fallback_rmn)
                print("OTP Generated successfully")
            else:
                print(msg)

        else:
            print("Failed to generate OTP")
            return False


def loginWithPass(sid, rmn, pwd):
    # For login but sid and rmn must be present
    payload = getPayload(auth=pwd, sid=sid, loginOpt="PWD", rmn=rmn)
    headers = getHeaders()
    x = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    if x.status_code == 200:
        responseMessage = x.json()['message']
        responseData = x.json()['data']
        if responseMessage == "Logged in successfully.":
            print(responseMessage)
            user.update({
                "accessToken": responseData['accessToken'],
                "entitlements": responseData['userDetails']['entitlements'],
                "sid": responseData['userDetails']['sid'],
                "sName": responseData['userDetails']['sName'],
                "acStatus": responseData['userDetails']['acStatus'],
                "profileId": responseData['userProfile']['id']
            })
            saveUserDetailsToFile()
        else:
            print(responseMessage)
    else:
        print("Failed to login ")


def loginWithOTP(sid, rmn, otp):
    # For login both sid and rmn must be present
    if sid == "":
        sid = lookupSid(rmn)
    if rmn == "":
        rmn = fallback_rmn
    payload = getPayload(auth=otp, sid=sid, loginOpt="OTP", rmn=rmn)
    headers = getHeaders()
    x = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    if x.status_code == 200:
        responseMessage = x.json()['message']
        responseData = x.json()['data']
        if responseMessage == "Logged in successfully.":
            print(responseMessage)
            user.update({
                "accessToken": responseData['accessToken'],
                "entitlements": responseData['userDetails']['entitlements'],
                "sid": responseData['userDetails']['sid'],
                "sName": responseData['userDetails']['sName'],
                "acStatus": responseData['userDetails']['acStatus'],
                "profileId": responseData['userProfile']['id']
            })
            saveUserDetailsToFile()
        else:
            print(responseMessage)
    else:
        print("Failed to login ")


def getPayload(auth, sid, loginOpt, rmn):
    return {
        "authorization": auth,
        "rmn": rmn,
        "sid": sid,
        "loginOption": loginOpt
    }


def getHeaders():
    headers = {
        'x-app-id': 'ott-app',
        'x-app-key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6ImR2ci11aSIsImtleSI6IiJ9'
                     '.XUQUYRo82fD_6yZ9ZEWcJkc0Os1IKbpzynLzSRtQJ-E',
        'x-api-key': '9a8087f911b248c7945b926f254c833b',
        'device_details': '{"app":"11.0","lo":"en_IN","os":"10",'
                          '"device_id":"YVJNVFZWVlZ7S01UZmRZTWNNQ3lHe0RvS0VYS0NHSwA","ip":"","dn":"ONEPLUS A6003",'
                          '"device_type":"ANDROID","device_category":"open","manufacturer":"OnePlus","ma":"",'
                          '"car":"","sname":"","device_platform":"MOBILE","location":"","model":"ONEPLUS A6003",'
                          '"pl":"Android","net":"Wifi"}',
        'Content-Type': 'application/json',
        'User-Agent': 'PostmanRuntime/7.26.10'
    }
    return headers


def saveUserDetailsToFile():
    with open('userDetails.json', 'w') as userDetailsFile:
        json.dump(user, userDetailsFile)


def lookupSid(rmn):
    url = API_BASE_URL + "rest-api/pub/api/v1/subscriberLookup" + "?rmn=" + rmn

    x = requests.get(url)
    msg = x.json()['code']
    if msg == "We are unable to process your request. Please try again later.":
        sid = x.json()['data']['sidList'][0]["sid"]
        return sid
    else:
        print("Could not get Subscribed ID.. Message:", msg)
        exit(0)
