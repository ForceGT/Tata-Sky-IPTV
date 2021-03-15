from constants import API_BASE_URL
import requests
import json


def getUserDetails():
    with open("userDetails.json", "r") as userDetailFile:
        userDetails = json.load(userDetailFile)
    return userDetails


def getChannelList():
    with open('allChannels.json', 'r') as allChannelsFile:
        channelList = json.load(allChannelsFile)
    return channelList


def generateJWT(channelId):
    url = API_BASE_URL + "auth-service/v1/oauth/token-service/token"
    payload = json.dumps(getPayloadForJWT(channelId))
    headers = getHeaders()
    x = requests.request("POST", url, headers=headers, data=payload)

    if x.status_code == 200:
        msg = x.json()['message']
        if msg == 'OAuth Token Generated Successfully':
            print(msg + " for channelId:" + str(channelId))

            token = x.json()['data']['token']
            print("Token:", token)
            return token
        else:
            print(msg)
            return ""
    else:
        print("Response:", x.text)
        print("Could not generate JWT for channelId:", channelId)
        return ""


def getPayloadForJWT(channelId):
    return {
        "action": "stream",
        "epids": getEpidList(channelId)
    }


def getUserChannelSubscribedList():
    included = []
    userDetails = getUserDetails()
    entitlements = [entitlement['pkgId'] for entitlement in userDetails["entitlements"]]
    channelList = getChannelList()
    for channel in channelList:
        for userEntitlement in entitlements:
            if userEntitlement in channel['channel_entitlements']:
                included.append(channel)
    with open('userSubscribedChannels.json', 'w') as userSubChannelFile:
        json.dump(included, userSubChannelFile)

    return included


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
            print("Entitlement found:", entitlement)
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
    generateJWT(78)
