import login
import utils
import jwtoken as jwt
import requests

while True:
    try:
        userDetails = jwt.getUserDetails()
    except FileNotFoundError:
        logged_in = "false"
    else:
        logged_in = userDetails["loggedIn"]

    s = utils.getPrintNote()
    print(s if logged_in != "true" else "")
    print("Credits: Gaurav Thakkar (My Github is: https://github.com/ForceGT)" if logged_in != "true" else "")
    print("====================================")
    print(" Login Status: " + logged_in)
    print("====================================")
    print("Menu:")
    print("1. Login using Password" if logged_in != "true" else "1. Login Again Using Password")
    print("2. Login using OTP" if logged_in != "true" else "2. Login Again Using OTP")
    print("3. Generate my playlist ")
    print("4. Exit")
    print("*************************************************************")
    print("\n")
    try:
        ch = int(input("Enter your choice:"))
    except (EOFError, KeyboardInterrupt):
        print("")
        ch = 4

    if ch == 1:
        rmn = str(input("Enter your Registered Mobile Number without the country code: "))
        try:
            r = requests.post('https://tm.tapi.videoready.tv/rest-api/pub/api/v2/subscriberLookup', json={"rmn": rmn}, timeout=10)
            resp = r.json()
            if resp['code'] != 0: raise ValueError # Usually invalid RMN
            sids = [ i['sid'] for i in resp['data']['sidList']]
            if len(sids) > 1:
                print("Multiple Subscriber IDs found for this RMN:")
                print("\n".join(sids))
                raise Exception("Need to manually select the SID")
            sid = str(input("Enter your Subscriber Id [" + sids[0] + "]: ")) or sids[0]
        except:
            sid = str(input("Enter your Subscriber Id: "))
        pwd = str(input("Enter your password: "))
        print("Trying to Login with password ............")
        print("\n \n")
        print("*************************************")
        login.loginWithPass(sid=sid, rmn=rmn, pwd=pwd)
    elif ch == 2:
        rmn = str(input("Enter your Registered Mobile No without the Country Code: "))
        try:
            r = requests.post('https://tm.tapi.videoready.tv/rest-api/pub/api/v2/subscriberLookup', json={"rmn": rmn}, timeout=10)
            resp = r.json()
            if resp['code'] != 0: raise ValueError # Usually invalid RMN
            sids = [ i['sid'] for i in resp['data']['sidList']]
            if len(sids) > 1:
                print("Multiple Subscriber IDs found for this RMN:")
                print("\n".join(sids))
                raise Exception("Need to manually select the SID")
            sid = str(input("Enter your Subscriber Id [" + sids[0] + "]: ")) or sids[0]
        except:
            sid = str(input("Enter your Subscriber Id: "))
        login.generateOTP(sid=sid, rmn=rmn)
        otp = str(input("Enter the OTP sent to your rmn: "))
        print("\n \n")
        print("*************************************")
        print("Trying to Login with OTP ................")
        login.loginWithOTP(sid=sid, rmn=rmn, otp=otp)
    elif ch == 3:
        if logged_in == "true":
            print("***********************")
            print("Please wait till the playlist is generated...")
            print("You may see a lot of lines being printed, you may ignore it")
            print("The generated m3u will be saved as allChannelPlaylist.m3u under the code_samples directory")
            print("************************************")
            utils.m3ugen()
        else:
            print("Please login with options 1 or 2 before generating playlist")
    elif ch == 4:
        print("Bye Bye.. See you soon!")
        exit()
    else:
        print("Wrong input entered ... Exiting")
        exit(1)
