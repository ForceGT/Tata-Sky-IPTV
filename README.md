# Tata Sky/ Play IPTV Script generator

A script to generate the m3u playlist containing direct streamable file (.mpd or MPEG-DASH or DASH) 
based on the channels that the user has subscribed on the Tata Sky portal.

[![GitHub forks](https://img.shields.io/github/forks/ForceGT/Tata-Sky-IPTV?logo=forks&style=plastic)](https://github.com/ForceGT/Tata-Sky-IPTV/network) [![GitHub stars](https://img.shields.io/github/stars/ForceGT/Tata-Sky-IPTV)](https://github.com/ForceGT/Tata-Sky-IPTV/stargazers) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)  [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)


## NOT MAINTAINED ANYMORE, BECAUSE MOST OF THE STUFF HAS BEEN PATCHED

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
Find some good M3u players [here](docs/m3uplayers.md)

## Auto Generating Playlists in 24 hours
- Take a look at [Shravan's Idea](https://github.com/Shra1V32/TataSky-Playlist-AutoUpdater)
- Take a look at [Saif's Idea](https://github.com/saifshaikh1805/tata-sky-m3u)

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
