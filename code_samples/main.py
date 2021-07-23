import login
import utils
import jwtoken as jwt

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
    ch = int(input("Enter your choice:"))

    if ch == 1:
        rmn = str(input("Enter your Registered Mobile Number without the country code: "))
        sid = str(input("Enter your Subscriber Id: "))
        pwd = str(input("Enter your password: "))
        print("Trying to Login with password ............")
        print("\n \n")
        print("*************************************")
        login.loginWithPass(sid=sid, rmn=rmn, pwd=pwd)
    elif ch == 2:
        rmn = str(input("Enter your Registered Mobile No without the Country Code: "))
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
