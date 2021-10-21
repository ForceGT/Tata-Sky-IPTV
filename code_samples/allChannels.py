### Script to get all channels from tata sky
import threading
import requests
import json as json

API_BASE_URL = "https://kong-tatasky.videoready.tv/"

channel_list = []


def getChannelInfo(channelId):
    url = "{}content-detail/pub/api/v1/channels/{}".format(API_BASE_URL, channelId)
    x = requests.get(url)
    channel_meta = x.json()['data']['meta'][0]
    channel_detail_dict = x.json()['data']['detail']
    onechannl = {
        "channel_id": str(channelId),
        "channel_name": channel_meta.get('channelName', ''),
        "channel_license_url": channel_detail_dict.get('dashWidewineLicenseUrl', ''),
        "channel_url": channel_detail_dict.get('dashWidewinePlayUrl', ''),
        "channel_entitlements": channel_detail_dict.get('entitlements', ''),
        "channel_logo": channel_meta.get('channelLogo', ''),
        "channel_genre": channel_meta.get('primaryGenre',"")
    }
    channel_list.append(onechannl)


def saveChannelsToFile():
    new_channel_list = sorted(channel_list, key = lambda i: i['channel_id'])
    print(len(channel_list))
    print(len(new_channel_list))
    with open("allChannels.json", "w") as channel_list_file:
        json.dump(new_channel_list, channel_list_file)
        channel_list_file.close()


def processChnuks(channel_lists):
    try:
        for channel in channel_list:
            print("Getting channelId:{}".format(channel.get('id', '')))
            channel_id = str(channel.get('id', ''))
            getChannelInfo(channel_id)
    except:
        print("exception on channel id " + str(channel.get('id', '')))


def getAllChannels():
    ts = []
    url = API_BASE_URL + "content-detail/pub/api/v1/channels?limit=534"
    x = requests.get(url)
    channel_list = x.json()['data']['list']
    print("Total Channels fetched:", len(channel_list))
    print("Fetching channel info..........")
    for i in range(len(channel_list)):
        t = threading.Thread(target=processChnuks, args=([channel_list[i:i + 1]]))
        ts.append(t)
        t.start()
    for t in ts:
        t.join()
    print("Saving all to a file.... " + str(len(channel_list)))
    saveChannelsToFile()


if __name__ == '__main__':
    getAllChannels()
