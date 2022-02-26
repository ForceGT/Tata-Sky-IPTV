# Tata Sky/ Play IPTV Script generator

A script to generate the m3u playlist containing direct streamable file (.mpd or MPEG-DASH or DASH) 
based on the channels that the user has subscribed on the Tata Sky portal.

[![GitHub forks](https://img.shields.io/github/forks/ForceGT/Tata-Sky-IPTV?logo=forks&style=plastic)](https://github.com/ForceGT/Tata-Sky-IPTV/network) [![GitHub stars](https://img.shields.io/github/stars/ForceGT/Tata-Sky-IPTV)](https://github.com/ForceGT/Tata-Sky-IPTV/stargazers) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)  [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

## Requirements

+ A working brain
+ Knowledge of basic python
+ A working Tata Sky/ Play account
+ Channels that you want to watch, already subscribed **(I'm sorry, no freebies)**
+ An app capable of reading a [m3u](https://docs.fileformat.com/audio/m3u/) file

## How to use
I know you would love to get your hands on how this works, but hold on and read before you proceed further
 > The methods are divided into `Easy` and `Difficult` based on how comfortable you are with the commandline. The `Easy` guide is recommended if you have no working knowledge of Python or scripting in general
## The Easy Way (Using an App)

- Login with your SID, RMN and OTP/ Password(deprecated) first
- Once you login, your details are saved to your local storage so that you don't have to enter the details again and again
- Every 24 hours, the playlist expires, so the app gives you the next expiry time and you will have to generate your playlist again before that time
- The app can be found in the [releases page](https://github.com/ForceGT/Tata-Sky-IPTV/releases)
```
Minimum Supported  Android Version : Android 5.0
```

## The Difficult Way (Using a Script)
### Setting up your environment

+ Make sure you have [python](https://www.python.org/downloads/) up and running on your system. **If you don't know how to do this then well, don't think of proceeding further**
+ You need `requests` to be installed. Do that by using ``pip install requests``

### Running the scripts
+ Clone this to your directory using ```git clone https://github.com/ForceGT/TSPrivateAPI``` or download the `zip` file and then go inside the `code_samples` directory and open your terminal there
+ Change to the ```code_samples``` directory by using  ```cd code_samples```
+ Simply run ```main.py``` (the main script) using the following code
```python
    python main.py
```
+ You will get options to login using the different methods, upon successful login a ```userDetails.json``` file is created which contains important details of the user. The ```accessToken``` has to be updated from time to time. To do so run the login logic again. If you delete the ```userDetails.json``` file you will have to login again so please be careful 

+ You can generate m3u file by selecting option 3. This generates ```allChannelPlaylist.m3u``` file in the current directory.**NOTE: Please run this only after logging in using Step 1 or 2 otherwise the script exits with an error**

+ You need to login just once usually, it will create a `userDetails.json` file once you login, and then you can just regenerate the playlist each day when you would like to use it. If you don't see the `userDetails.json` file anywhere, then you may have to login again


## Some Good M3U Players for different platforms

### Android/ Android TV
- [Tivimate](https://play.google.com/store/apps/details?id=ar.tvplayer.tv&hl=en_IN&gl=US) is a fantastic app that works well with both `TV` and `Mobile`
- [OTT Navigator](https://play.google.com/store/apps/details?id=studio.scillarium.ottnavigator&hl=en_IN&gl=US) : `TV` 
- [Kodi](https://kodi.tv/): `TV` and `Mobile`
- [NS Player](https://play.google.com/store/apps/details?id=com.genuine.leone) is `recommended` for `Mobile`

> Caution : Kodi acts weirdly sometimes, so use it at your own risk

### Desktops
- Currently no desktop player has support for DASH with DRM. If you know of such an app let me know

### Web
- There is no support for playing m3u as a playlist, however you can take an individual channel from your generated m3u and play it

#### Playing in a browser (tried with Chrome)

+ I personally use [Native MPEG-Dash + HLS Playback](https://chrome.google.com/webstore/detail/native-mpeg-dash-%20-hls-pl/cjfbmleiaobegagekpmlhmaadepdeedn) which doesn't suppport playlists yet

See the below section on `Getting hold of individual channels` to know how to get the link to play a specific channel as you cannot play the entire playlist
+ Get the channel url (ends with ```.mpd```) and paste it in the browser
+ The extension automatically asks for the license url. You should then input the  license url.

#### Getting hold of individual channels
- Just open the m3u file generated above in any text editor of your choice and search for your channel using the search functionality of your editor
- The channel url is the one that starts with `https`and ends with ```.mpd``` 
- The license url following the `#KODIPROP:inputstream.adaptive.license_key=` field
- The license url and the channel url are the only two fields needed to play the channel 




## How it works

If you're interested in how this mechanism works, Refer to [docs](docs/working.md)



## Discussion and Support 
[![homepage][1]][2]

[1]:  images/telegram.png
[2]:  https://T.me/tskyiptv

## License and Disclosures

This code is just a CASE STUDY on how the authentication mechanism and live streaming using IPTV works
I am in no way responsible if you misuse the code and cause revenue loss to the concerned parties and owners of the portal

This code is protected under the [MIT](https://opensource.org/licenses/MIT) license