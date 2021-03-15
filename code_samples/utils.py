import threading
import jwtoken
import time

m3ustr = "#EXTM3U \n\n"


def m3ugen(m3ustr=m3ustr):
    channelList = jwtoken.getUserChannelSubscribedList()
    kodiPropLicenseType = "#KODIPROP:inputstream.adaptive.license_type=com.widevine.alpha"
    kodiPropLicenseUrl = ""
    for channel in channelList:
        ls_session_key = jwtoken.generateJWT(channel['channel_id'])
        if ls_session_key != "":
            licenseUrl = channel['channel_license_url'] + "&ls_session=" + ls_session_key
            kodiPropLicenseUrl = "#KODIPROP:inputstream.adaptive.license_key=" + licenseUrl
        else:
            print("Didnt't get license for channel: Id: {0} Name:{1}".format(channel['channel_id'],
                                                                             channel['channel_name']))
            print('Continuing...Please get license manually')
        m3ustr += kodiPropLicenseType + "\n" + kodiPropLicenseUrl + "\n" + "#EXTINF:-1 "
        m3ustr += "tvg-id=" + "\"" + channel['channel_id'] + "\" " + "tvg-logo=\"" + channel[
            'channel_logo'] + "\" ," + "\n" + channel['channel_url'] + "\n\n"

    saveM3ustringtofile(m3ustr)


def saveM3ustringtofile(m3ustr):
    with open("allChannelPlaylist.m3u", "w") as allChannelPlaylistFile:
        allChannelPlaylistFile.write(m3ustr)


if __name__ == '__main__':
    m3ugen()
