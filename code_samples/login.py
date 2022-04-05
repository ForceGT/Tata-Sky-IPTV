from constants import API_BASE_URL, API_BASE_URL_2, HEADER_X_APP_ID, HEADER_X_APP_KEY, HEADER_X_DEVICE_ID, HEADER_X_DEVICE_PLATFORM, \
    HEADER_X_DEVICE_TYPE, HEADER_X_API_KEY
import requests
import json
import argparse

url = API_BASE_URL_2 + "rest-api/pub/api/v3/login/ott"
fallback_rmn = ""
user = {}


def generateOTP(sid, rmn):
    print("Generating OTP.......")
    print("\n \n \n")
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
        return False


def loginWithPass(sid, rmn, pwd):
    payload = getPayload(auth=pwd, sid=sid, loginOpt="PWD", rmn=rmn)
    headers = getHeaders()
    x = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    if x.status_code == 200:
        responseMessage = x.json()['message']
        responseData = x.json()['data']
        if responseMessage == "Logged in successfully.":
            print(responseMessage)
            print("\n")
            print("**********************************************")
            print("Saving user details to userDetails.json so that you don't have to login again")

            user.update({
                "accessToken": responseData['accessToken'],
                "entitlements": responseData['userDetails']['entitlements'],
                "sid": responseData['userDetails']['sid'],
                "sName": responseData['userDetails']['sName'],
                "acStatus": responseData['userDetails']['acStatus'],
                "profileId": responseData['userProfile']['id'],
                "loggedIn": "true"
            })
            saveUserDetailsToFile()
        else:
            print(responseMessage)
    else:
        print("Failed to login ")


def loginWithOTP(sid, rmn, otp):
    payload = getPayload(auth=otp, sid=sid, loginOpt="OTP", rmn=rmn)
    headers = getHeaders()
    x = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    if x.status_code == 200:
        responseMessage = x.json()['message']
        responseData = x.json()['data']
        if responseMessage == "Logged in successfully.":
            print("**********************************************")
            print(responseMessage)
            print("\n")
            print("**********************************************")
            print("Saving user details to userDetails.json so that you don't have to login again")
            user.update({
                "accessToken": responseData['accessToken'],
                "expiresIn": responseData['expiresIn'],
                "entitlements": responseData['userDetails']['entitlements'],
                "sid": responseData['userDetails']['sid'],
                "sName": responseData['userDetails']['sName'],
                "acStatus": responseData['userDetails']['acStatus'],
                "profileId": responseData['userProfile']['id'],
                "loggedIn": "true"
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
        'authority': 'tm.tapi.videoready.tv',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'content-type': 'application/json',
        'device_details': '{"pl":"web","os":"WINDOWS","lo":"en-us","app":"1.36.09","dn":"PC",'
                          '"bv":100,"bn":"CHROME","device_id":"a13ce448c87mar1486c369843c30e4331638560148363",'
                          '"device_type":"WEB","device_platform":"PC","device_category":"open",'
                          '"manufacturer":"WINDOWS_CHROME_100","model":"PC","sname":""}'
        'origin': 'https://watch.tataplay.com',
        'referer': 'https://watch.tataplay.com/'
    }
    return headers


def saveUserDetailsToFile():
    with open('userDetails.json', 'w') as userDetailsFile:
        json.dump(user, userDetailsFile)


# This method looks up Subscriber ID from registered mobile number
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--otp", type=int, help="OTP for Login", required=True)
    parser.add_argument("--sid", type=int, help="The Subscriber ID for login", required=True)
    parser.add_argument("--rmn", type=int, help="The Registered Mobile Number for login", required=True)
    args = parser.parse_args()
    print(f'Entered Params: SID:{args.sid}, RMN:{args.rmn}, OTP: {args.otp}')
    print("Logging in with OTP....")
    loginWithOTP(sid=args.sid, rmn=args.rmn, otp=args.otp)
