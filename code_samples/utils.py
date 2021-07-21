import jwtoken
import threading

m3ustr = "#EXTM3U \n\n"
kodiPropLicenseType = "#KODIPROP:inputstream.adaptive.license_type=com.widevine.alpha"


def processTokenChunks(channelList):
    global m3ustr
    kodiPropLicenseUrl = ""
    if not channelList:
        print("Channel List is empty ..Exiting")
        exit(1)
    for channel in channelList:
        ls_session_key = jwtoken.generateJWT(channel['channel_id'], iterative=False)
        if ls_session_key != "":
            licenseUrl = channel['channel_license_url'] + "&ls_session=" + ls_session_key
            kodiPropLicenseUrl = "#KODIPROP:inputstream.adaptive.license_key=" + licenseUrl
        else:
            print("Didn't get license for channel: Id: {0} Name:{1}".format(channel['channel_id'],
                                                                            channel['channel_name']))
            print('Continuing...Please get license manually for channel :', channel['channel_name'])
        m3ustr += kodiPropLicenseType + "\n" + kodiPropLicenseUrl + "\n" + "#EXTINF:-1 "
        m3ustr += "tvg-id=" + "\"" + channel['channel_id'] + "\" " + "tvg-logo=\"" + channel[
            'channel_logo'] + "\" ," + channel['channel_name'] + "\n" + channel['channel_url'] + "\n\n"


def m3ugen():
    ts = []
    global m3ustr
    channelList = jwtoken.getUserChannelSubscribedList()
    for i in range(0, len(channelList), 5):
        t = threading.Thread(target=processTokenChunks, args=([channelList[i:i + 5]]))
        ts.append(t)
        t.start()
    for t in ts:
        t.join()
    print("Found total {0} channels subscribed by user \n Saving them to m3u file".format(len(channelList)))
    saveM3ustringtofile(m3ustr)


def saveM3ustringtofile(m3ustr):
    with open("allChannelPlaylist.m3u", "w") as allChannelPlaylistFile:
        allChannelPlaylistFile.write(m3ustr)


if __name__ == '__main__':
    m3ugen()
