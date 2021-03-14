### Script to get all channels from tata sky
from TSPrivateAPI.code_samples.model.channel import Channel
from constants import API_BASE_URL, API_BASE_URL_2
import requests
import time
import json as json

channel_list = list()

def getAllChannels():
    url = API_BASE_URL + "content-detail/pub/api/v1/channels?limit=443"
    x = requests.get(url)
    channel_list = x.json()['data']['list']
    print("Total Channels fetched:", len(channel_list))
    print("Fetching channel info..........")
    for index, channel in enumerate(channel_list):
        print("Getting index: {0}, channelId: {1}".format(index, channel['id']))
        channel_id = str(channel['id'])
        getChannelInfo(channel_id)
    print("Saving all to a file....")
    saveChannelsToFile()




def getChannelInfo(channelId):
    url = API_BASE_URL + "content-detail/pub/api/v1/channels/" + channelId
    x = requests.get(url)
    channel_meta = x.json()['data']['meta'][0]
    channel_detail_dict = x.json()['data']['detail']
    channel_name = channel_meta['channelName']
    channel_license_url = channel_detail_dict['dashWidewineLicenseUrl']
    channel_url = channel_detail_dict['dashWidewinePlayUrl']
    channel_entitlements = channel_detail_dict['entitlements']
    channel_logo = channel_meta['channelLogo']

    channel = Channel(channel_name, channel_entitlements, channel_logo, channel_url, channel_license_url)
    channel_list.append(channel)

    time.sleep(5)


def saveChannelsToFile():
    with open("allchannels.txt", "w") as channel_list_file:
        channel_list_file.write("{0:10}  {1:14}   {3}\n".format("Channel Name", "Channel Streamable Url", "Channel License Url"))
        for channel in channel_list:
            channel_list_file.write("{0:10}  {1:14}   {3}\n".format(channel.name, channel.url, channel.license_url))



if __name__ == '__main__':
    getAllChannels()
