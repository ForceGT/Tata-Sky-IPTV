from constants import API_BASE_URL
import requests
import json
import base64
import time


# This method gets the userDetails from the userDetails file and returns it as a dictionary
def getUserDetails():
    with open("userDetails.json", "r") as userDetailFile:
        userDetails = json.load(userDetailFile)
    return userDetails


# This method gets the channelList from the allChannels.json file and returns it as a list/dictionary
def getChannelList():
    return json.load(open("allChannels.json", "r"))

# This method will generate a jwt based on the supplied channelId
# It involves sending a post request to a specific endpoint with some headers and params
# The token expires in a day
def generateJWT(channelId, iterative=True):
    url = API_BASE_URL + "auth-service/v1/oauth/token-service/token"
    payload = json.dumps(getPayloadForJWT(channelId))
    headers = getHeaders()
    x = requests.request("POST", url, headers=headers, data=payload)

    if x.status_code == 200:
        msg = x.json()['message']
        if msg == 'OAuth Token Generated Successfully':
            # doesn't print the msg in iterative state
            s = msg + " for channelId: " + str(channelId)
            if iterative:
                print(s)

            token = x.json()['data']['token']
            tokenMsg = "Token:" + token
            if iterative:
                print(tokenMsg)
            return token
        else:
            print(msg)
            return ""
    else:
        print("Response:", x.text)
        print("Could not generate JWT for channelId:", channelId)
        return ""


# This method will get the payload needed for the jwt generation
# Involves sending the episode ids
def getPayloadForJWT(channelId):
    return {
        "action": "stream",
        "epids": getEpidList(channelId)
    }

def getPayloadForCommonJWT():
    epidList = getCommonEpidList()
    multipleEpid = len(epidList) > 1
    payloads = [{
        "action": "stream",
        "epids": epid
    } for epid in epidList] if multipleEpid else [{
        "action": "stream",
        "epids": epidList
    }]
    return payloads
            

# This method returns and also saves all the subscribed channels based on the users choices in the tatasky portal It
# checks the user entitlements in all the channel entitlements and keeps the channel if a specific user entitlement
# has been found
def getUserChannelSubscribedList():
    included = []
    userDetails = getUserDetails()
    entitlements = [entitlement['pkgId'] for entitlement in
                    userDetails["entitlements"]]  # all the user entitlements saved in userDetails.json
    channelList = getChannelList()  # All the channels saved in allChannels.json
    for channel in channelList:
        for userEntitlement in entitlements:
            if userEntitlement in channel['channel_entitlements']:
                included.append(channel)
    with open('userSubscribedChannels.json', 'w') as userSubChannelFile:
        json.dump(included, userSubChannelFile)

    return included


# This method gets the needed epid or the entitlement/episode id
# This is included in the payload to get the jwt

def getEpidList(channelId):
    epidList = []
    selectedChannel = {}
    includedChannels = getUserChannelSubscribedList()
    for channel in includedChannels:
        if channel['channel_id'] == str(channelId):
            selectedChannel.update(channel)
    userDetails = getUserDetails()
    entitlements = [entitlement['pkgId'] for entitlement in userDetails["entitlements"]]
    for entitlement in entitlements:
        if entitlement in selectedChannel['channel_entitlements']:
            epidList.append({
                "epid": "Subscription",
                "bid": entitlement
            })
    return epidList

# Decodes the token and returns the epid list
def extractEpidsFromToken(token):
    bidList = []
    data = token.split(".")[1]
    epids = base64.b64decode(data + "==").decode('utf-8')
    epidList = json.loads(epids)
    for epid in epidList['ent']:
        bidList.append(epid['bid'])
    return bidList

def getCommonEpidList() -> list:
    epidList = []
    groupedEpidList = []
    userDetails = getUserDetails()
    entitlements = [entitlement['pkgId'] for entitlement in userDetails["entitlements"]]
    if len(entitlements) > 5:
        # Group the entitlements into chunks of 8
        groupedEntitlements = [entitlements[i:i + 5] for i in range(0, len(entitlements), 5)]
        for groupedEntitlement in groupedEntitlements:
            epidList = []
            for entitlement in groupedEntitlement:
                epidList.append({
                    "epid": "Subscription",
                    "bid": entitlement
                })
            groupedEpidList.append(epidList)
        return groupedEpidList
    for entitlement in entitlements:
        epidList.append({
            "epid": "Subscription",
            "bid": entitlement
        })
    return epidList

def generateToken(url, headers, payload):
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        msg = response.json()['message']
        if msg == 'OAuth Token Generated Successfully':
            return response.json()['data']['token']
    elif response.status_code == 429 and response.json()['message'] == 'API rate limit exceeded':
        return "Rate Limit Exceeded"
    return ""

def getCommonJwt():
    url = API_BASE_URL + "auth-service/v1/oauth/token-service/token"
    payloads = getPayloadForCommonJWT()
    tokens = []
    count = 0
    for payload in payloads:
        headers = getHeaders()
        token = generateToken(url, headers, payload)
        count += 1
        while token == "Rate Limit Exceeded":
            print(f"Rate Limit Exceeded for count {str(count)}, Retrying in 8 seconds...")
            time.sleep(8)  # Wait for 60 seconds before retrying
            token = generateToken(url, headers, payload)
        if token:
            tokens.append(token)
    return tokens


def getHeaders():
    userDetails = getUserDetails()
    accessToken = userDetails['accessToken']
    subsId = userDetails['sid']
    sName = userDetails['sName']
    profileId = userDetails['profileId']
    headers = {
    'authority': 'tm.tapi.videoready.tv',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'authorization': 'bearer ' + accessToken,
    'content-type': 'application/json',
    'device_details': '{"pl":"web","os":"WINDOWS","lo":"en-us","app":"1.36.35","dn":"PC","bv":103,"bn":"CHROME","device_id":"YVJNVFZWVlZ7S01UZmRZTWNNQ3lHe0RvS0VYS0NHSwA","device_type":"WEB","device_platform":"PC","device_category":"open","manufacturer":"WINDOWS_CHROME_103","model":"PC","sname":"%s"}' % sName,
    'kp': 'false',
    'locale': 'ENG',
    'origin': 'https://watch.tataplay.com',
    'platform': 'web',
    'profileid': str(profileId),
    'referer': 'https://watch.tataplay.com/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36',
    'x-device-id': 'YVJNVFZWVlZ7S01UZmRZTWNNQ3lHe0RvS0VYS0NHSwA',
    'x-device-platform': 'PC',
    'x-device-type': 'WEB',
    'x-subscriber-id': str(subsId),
    'x-subscriber-name': str(sName)
    }
    return headers


if __name__ == '__main__':
    channel_id = str(input("Enter the channelId for which you want to generate the token"))
    generateJWT(channel_id)
