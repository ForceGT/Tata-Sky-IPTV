### Script to get all channels from tata sky
from TSPrivateAPI.code_samples.model.channel import Channel
from constants import API_BASE_URL, API_BASE_URL_2
import requests
import json as json

channel_list = list()

def getAllChannels():
    url = API_BASE_URL + "content-detail/pub/api/v1/channels?limit=443"
    x = requests.get(url)
    channel_list = x.json()['data']['list']
    print("Total Channels fetched:", len(channel_list))
    print("Fetching channel info..........")
    for channel in channel_list:
        channel_id = str(channel['id'])
        getChannelInfo(channel_id)




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

    channel = Channel(channel_name,channel_entitlements, channel_logo,channel_url, channel_license_url)
    channel_list.append(channel)


if __name__ == '__main__':
    getAllChannels()
