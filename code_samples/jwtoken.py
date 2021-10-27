from constants import API_BASE_URL
import requests
import json


# This method gets the userDetails from the userDetails file and returns it as a dictionary
def getUserDetails():
    with open("userDetails.json", "r") as userDetailFile:
        userDetails = json.load(userDetailFile)
    return userDetails


# This method gets the channelList from the allChannels.json file and returns it as a list/dictionary
def getChannelList():
    with open('allChannels.json', 'r') as allChannelsFile:
        channelList = json.load(allChannelsFile)
    return channelList


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


def getHeaders():
    userDetails = getUserDetails()
    accessToken = userDetails['accessToken']
    subsId = userDetails['sid']
    sName = userDetails['sName']
    headers = {
        'Authorization': 'bearer ' + accessToken,
        'x-subscriber-id': str(subsId),
        'x-app-id': 'ott-app',
        'x-app-key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6ImR2ci11aSIsImtleSI6IiJ9.XUQUYRo82fD_6yZ9ZEWcJkc0Os1IKbpzynLzSRtQJ-E',
        'x-subscriber-name': str(sName),
        'x-api-key': '9a8087f911b248c7945b926f254c833b',
        'x-device-id': 'YVJNVFZWVlZ7S01UZmRZTWNNQ3lHe0RvS0VYS0NHSwA',
        'x-device-platform': 'MOBILE',
        'x-device-type': 'ANDROID',
        'Content-Type': 'application/json',
        'User-Agent': 'PostmanRuntime/7.26.10'
    }
    return headers


if __name__ == '__main__':
    channel_id = str(input("Enter the channelId for which you want to generate the token"))
    generateJWT(channel_id)
