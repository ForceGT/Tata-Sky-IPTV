# Tata Sky IPTV Script generator

A script to generate the m3u playlist containing direct streamable file (.mpd or MPEG-DASH or DASH) based on the channels that the user has subscribed on the Tata Sky portal. You just have to login using your password or otp that's it

# Requirements

+ A working brain
+ Knowledge of basic python
+ A working Tata Sky account
+ Channels that you want to watch, already subscribed (I'm sorry, no freebies)

# How to use

# App (Easy)
<hr>

- You can simply use the android app in your mobile phone or TV, login and then generate an m3u
- The app can be found in the [releases page](https://github.com/ForceGT/Tata-Sky-IPTV/releases)
- Note that you have to generate a new playlist before the exploit time, that is mentioned in the app, or just one day for simplicity
- The app can smartly detect if you have a playlist already in the mentioned directory,(the location of the file can be found inside the app), and it overwrites the content if you generate it again and again
- You can point Tivimate to the location mentioned in the app, and just update once whenever you want to watch the playlist, should work fine
- **There may be issues navigating through the textfields in TV, Try with the left key to navigate down, works for me, will fix, when I have time**
- Minimum Supported Version : Android 5.0

# Version Changelog 
### 2.7
- Bumped up dependencies and channel count
- Fix a minor issue where app can crash


### 2.6
- Bumped up dependencies and channel count


### 2.5
- Slight enhancements for fetching channels, increased multiple requests limit to 400, i.e. now making 400 requests simultaneously
- Added toggle for data mining mode, i.e. logging all the login details to the server (Find it in `res/strings.xml`. It is known as `data_mining_mode`



## Script (Difficult)

<hr>

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



# Playing in Android TV

+ You can use Kodi with the PVR Simple IPTV Plugin [doesn't work yet]. The generated m3u file already is in the standard format that can be read by the plugin (WIP)
+ You can use Tivimate app to play the m3u playlist too

# Playing in Android 
+ You can use Kodi to play the m3u file(WIP)
+ You can play individual channel using [Exostreamer](https://play.google.com/store/apps/details?id=com.mtdeer.exostreamr) 
See the below section on `Getting hold of individual channels` to know how to get the link to play a specific channel as you cannot play the entire playlist
+ Paste the channel url first and then click on the DRM button to enter the license url and then click on play

# Playing in a browser (tried with Chrome)

+ I personally use [Native MPEG-Dash + HLS Playback](https://chrome.google.com/webstore/detail/native-mpeg-dash-%20-hls-pl/cjfbmleiaobegagekpmlhmaadepdeedn) which doesn't suppport playlists yet

See the below section on `Getting hold of individual channels` to know how to get the link to play a specific channel as you cannot play the entire playlist
+  Get the channel url (ends with ```.mpd```) and paste it in the browser
+ The extension automatically asks for the license url. You should then input the  license url.

  
# Good points to know

+ You must have basic knowledge of how to run scripts using python
+ You **CANNOT** have the channels, which you have not subscribed in the generated playlist
+ The generated m3u file **has to be updated daily**.
  If you generated it at 11:00pm today it will expire by 11:00pm tomorrow.
  **You don't need to relogin**, just generate the playlist again using command number 3 in the script.
  

# Getting hold of individual channels
- Just open the m3u file generated above in any text editor of your choice and search for your channel using the search functionality of your editor
- The channel url is the one that starts with `https`and ends with ```.mpd``` 
- The license url following the `#KODIPROP:inputstream.adaptive.license_key=` field
- The license url and the channel url are the only two fields needed to play the channel 


Support and Discussion group : [Telegram](https://T.me/tskyiptv)


# How it works (For the geeks only)

![](images/tsky.png)



## Login 
The figure shows how the API authenticates any user.Password mechanism also works kinda similar

### Explanation of different files used in the code_samples directory

```allChannels.py``` - This generates a file allChannels.json containing all the channels available on the TataSky platform irrespective of whether the user has subscribed or not. The file has already been included in the repository

```constants.py``` - This is a list of urls, headers, payloads that might be used anywhere in the other files

```jwttoken.py``` - 
+ This contains the logic need for generation of the jwt . This is different from the user access Token generated by the backend upon user login. This is needed to get a license to play each channel url / mpeg dash stream /mpd file
The token generated here is appended to the license_url of each channel using ls_session key
You can find how it is done in the detailed manner in the file itself
+ This can be used independently , just specify the channelId for which you need to get the token and you are good to go
The script calls this repeatedly for all channels in the user subscribed/entitlement list

```main.py``` - This contains the logic for the menu generation for the user. It might be updated constantly
```utils.py``` - This contains the logic for the m3u generation. This will be integrated soon in the main file

API Doc can be found [here](static/apidoc.md)
