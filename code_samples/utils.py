# Generates Kodi playlist by default, If you want OTT Navigator Supported Playlist, pass '--ott-navigator' as argument.
import jwtoken as jwt
import threading
import sys
import requests

isOttNavigator = False
args = len(sys.argv)

if args == 2 and sys.argv[1] == '--ott-navigator':
    isOttNavigator = True

m3ustr = '#EXTM3U  x-tvg-url="https://www.tsepg.cf/epg.xml.gz" \n\n'
kodiPropLicenseType = "#KODIPROP:inputstream.adaptive.license_type=com.widevine.alpha"

# Checks for the common elements in two lists
def has_common_element(list1, list2):
    return any(item in list2 for item in list1)

def find_matching_token(channel):
    epidList = jwt.getEpidList(channel['channel_id'])
    for token, epids in tokensWithEpids.items():
        if has_common_element([epid['bid'] for epid in epidList], epids):
            return token
    return None, None

def processTokenChunks(channelList):
    global m3ustr
    if not channelList:
        print("Channel List is empty ..Exiting")
        exit(1)

    for channel in channelList:
        token = find_matching_token(channel)
        
        if token is None:
            print("Could not find a token for channel: " + channel['channel_name'])
            continue

        licenseUrl = channel['channel_license_url'] + "&ls_session=" + token
        kodiPropLicenseUrl = "#KODIPROP:inputstream.adaptive.license_key=" + licenseUrl
        if not isOttNavigator:
            kodiPropLicenseUrl += "|Content-Type=application/octet-stream|R{SSM}|"

        m3ustr += f"{kodiPropLicenseType}\n{kodiPropLicenseUrl}\n#EXTINF:-1 tvg-id=\"{channel['channel_id']}\" group-title=\"{channel['channel_genre']}\" tvg-logo=\"{channel['channel_logo']}\",{channel['channel_name']}\n{channel['channel_url']}\n\n"


def m3ugen():
    ts = []
    global m3ustr, commonJwt, tokensWithEpids
    with open("allChannels.json", "wb") as allChannelFile:
        response = requests.get("https://gist.githubusercontent.com/Shra1V32/ee918d53b2f0b65888809ba85f0e0183/raw/allChannels.json", timeout=15)
        allChannelFile.write(response.content)
    channelList = jwt.getUserChannelSubscribedList()
    commonJwt = jwt.getCommonJwt()
    tokensWithEpids = {}
    if not commonJwt:
        raise Exception("Could not generate common JWT")
    for token in commonJwt:
        tokensWithEpids[token] = jwt.extractEpidsFromToken(token) 

    for i in range(0, len(channelList), 5):
        t = threading.Thread(target=processTokenChunks, args=([channelList[i:i + 5]]))
        ts.append(t)
        t.start()
    for t in ts:
        t.join()

    print("================================================================")
    print("Found total {0} channels subscribed by user \nSaving them to m3u file".format(len(channelList)))
    print("================================================================")
    saveM3ustringtofile(m3ustr)


def saveM3ustringtofile(m3ustr):
    with open("allChannelPlaylist.m3u", "w") as allChannelPlaylistFile:
        allChannelPlaylistFile.write(m3ustr)


def getPrintNote():
    s = " *****************************************************\n" + "Welcome To TataSky Channel Generation Script\n" + \
        "**********************************************************\n" + \
        "- Using this script you can generate playable links based on the channels you have subscribed to \n" + \
        "- You can always read the README.md file if you don't know how to use the generated file \n" + \
        "- You can login using your password or generate an OTP. You need to enter both the Registered Mobile Number \n" + \
        "\n Caution: This doesn't promote any kind of hacking or compromising anyone's details"

    return s


if __name__ == '__main__':
    m3ugen()
