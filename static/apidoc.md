# Rough description of how the API works

This document seeks to tell you the main endpoints of the API based on whatever I could decipher

### Authentication

1.
Request Type| Endpoint | Meta | Params | Headers
------------ | -------| -----|---|---|
`POST`        |    https://ts-api.videoready.tv/rest-api/pub/api/v2/login/ott  |    Common API for login via RMN/SubID  | `raw json` authorization,rmn,sid,      loginOption: "PWD"/"OTP",pwd(optional)|`required` x-api-key,`required` x-app-key,`required` x-app-id , `required` device_details

**Detail Info** : 
+ device_details is a json object where keys `app`,`lo`,`os`,`device_id`,`ip`, `dn`,`device_type`,`device_category`,`manufacture`,`car`,`ma`,`pl`,`net`
are required for simulating mobile based login . 
+ Web based logins are different and they need different params
+ All the code can be found in the code_examples directory
+ Returns the access token and user entitlements which are of utmost importance in subsequent requests

2. 
Request Type | Endpoint | Meta | Params | Headers
---| ---| ---| ---|---|
`POST`| https://kong-tatasky.videoready.tv/auth-service/v1/oauth/token-service/token | JWT Token generation (needed for licensing) | `required` action , `required` epids | Authorization , x-subscriber-id, x-api-key, x-app-id, x-app-key, x-subscriber-name,x-device-id, x-device-platform, x-device-type

**Detail Info** : 
+ Params include information for what episode id (epid) the streaming license is needed
+ It returns a jwt token which expires in a day
+ All the code can be found in the code_examples directory


3. OTP Generation

a. *with sid*

Request Type| Endpoint | Meta | Params | Headers 
------------ | -------| -----|---|---|
`GET` | https://kong-tatasky.videoready.tv/rest-api/pub/api/v1/subscribers/{sid}/otp| Generate OTP using Sub ID| `sid` : subscriber id | None |

b. *with rmn*

Request Type| Endpoint | Meta | Params | Headers 
------------ | -------| -----|---|---|
`GET` | https://kong-tatasky.videoready.tv/rest-api/pub/api/v1/rmn/{rmn}/otp| Generate OTP using rmn| `rmn` : registered mobile number | None |

OTP validation can be done at 1


### Channels

1. All available channels

Request Type| Endpoint | Meta | Params | Headers 
------------ | -------| -----|---|---|
|`GET`|https://ts-api.videoready.tv/content-detail/pub/api/v1/channels | All available channels on the platform | limit = 443, offset | none

**Detail Info**:
+ The limit is set to 443 because max channel count is 443 (It may change in future). You can set it to any number 
+ You get a channel id with each channel in the list which can be utilised in the below endpoint

2. Channel info

 Request Type| Endpoint | Meta | Params | Headers 
------------ | -------| -----|---|---|
`GET` | https://kong-tatasky.videoready.tv/content-detail/pub/api/v1/channels/{{channelId}} | Links,episodes etc for each channel | channelId | None

**Detail Info** :
+ The channelId must be substituted from above
+ Response includes playable dash links, license url, episode ids etc
+ **IMPORTANT** License is granted only if the current user entitlements match the channel entitlements . This is a server side check while granting license
+ In  the response, `dashWidewinePlayUrl` is the dash playable url and `dashWidewineLicenseUrl` is the license url currently being used everywhere



## Miscellaneous Info 


To get a valid license take the `dashWidewineLicenseUrl` value and append to it `ls_session` where `ls_session` will be the token generated in Authentication Step 2

For example : 

`dashWidewineLicenseUrl`: "https://tatasky.live.ott.irdeto.com/Widevine/getlicense?CrmId=tatasky&AccountId=tatasky&ContentId=400000077"

and your jwt token generated in authentication endpoint number 2 is `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNvbnRyb2xfc2lnbmluZ19rZXlfcHJvZHVjdGlvbl8xNTk5MTYxMzc0NzY0In0.eyJzdWIiOiIxMjY3Nzg0MTM4IiwiaXNlIjp0cnVlLCJqdGkiOiJlNWJmMTVhZi0xNWM2LTQzNWUtYTU5MS04YjkzZjlkZmY5YmIiLCJhaWQiOiJ0Y` 

Then your valid license url becomes `https://tatasky.live.ott.irdeto.com/Widevine/getlicense?CrmId=tatasky&AccountId=tatasky&ContentId=400000077&ls_session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNvbnRyb2xfc2lnbmluZ19rZXlfcHJvZHVjdGlvbl8xNTk5MTYxMzc0NzY0In0.eyJzdWIiOiIxMjY3Nzg0MTM4IiwiaXNlIjp0cnVlLCJqdGkiOiJlNWJmMTVhZi0xNWM2LTQzNWUtYTU5MS04YjkzZjlkZmY5YmIiLCJhaWQiOiJ0Y`

#### How mpd works:

I know you don't want to get into the details of how dash/hls works but this is important to know if you get lost somewhere 

+ dash files or mpd files have segments which are a list of chunks and not the entire file since these are updated on the go while a live stream is on
+ After every x seconds dash players fetch a new segment which in turn has new chunk links 
+ According to the widewine policy, before fetching each chunk , the player has to verify if the right person gets the chunk and thus a license url is always needed to verify the same

#### How to use the links : 

+ Download https://chrome.google.com/webstore/detail/native-mpeg-dash-%20-hls-pl/cjfbmleiaobegagekpmlhmaadepdeedn or any other similar extension capable of playing dash/hls media 
+ Enter the `dashWidewinePlayUrl` in the address bar of your browser
+ When the extension asks for the licenseurl the supply the link as generated above





                                                                                                                     
                                                                                                                            
