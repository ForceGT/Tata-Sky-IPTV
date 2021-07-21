import login
import utils

logged_in = False

while True:
    print("Welcome To TataSky Channel Generation Script")
    print("#############################################")
    print("Using this script you can generate playable links based on the channels you have subscribed to \n This can "
          "also generate a m3u playlist based on your choice selection. You can always read the README.md file if you "
          "don't know how to use the generated file")
    print("You can login using your password or generate an OTP. You need to enter both the Registered Mobile Number("
          "rmn) "
          "as well as the Subscriber ID(sid) for using the script. Please go and get both before proceeding further")

    print("\n \n \n Caution: This doesn't promote any kind of hacking or compromising anyone's details. You use it at "
          "your own risk ")
    print("Menu:")
    print("1. Login using Password")
    print("2. Login using OTP")
    print("3. Generate my playlist ")
    print("4. Exit")
    print("Credits: Gaurav Thakkar (My Github is: https://github.com/ForceGT)")
    ch = int(input("Enter your choice:"))
    print(ch)
    if ch == 1:
        logged_in = True
        rmn = str(input("Enter your Registered Mobile Number without the country code: "))
        sid = str(input("Enter your Subscriber Id: "))
        pwd = str(input("Enter your password: "))
        print("Trying to Login with password ............")
        login.loginWithPass(sid=sid, rmn=rmn, pwd=pwd)
    elif ch == 2:
        logged_in = True
        rmn = str(input("Enter your Registered Mobile No without the Country Code: "))
        sid = str(input("Enter your Subscriber Id: "))
        login.generateOTP(sid=sid, rmn=rmn)
        otp = str(input("Enter the OTP sent to your rmn: "))
        print("Trying to Login with OTP ................")
        login.loginWithOTP(sid=sid, rmn=rmn, otp=otp)
    elif ch == 3:
        if logged_in:
            utils.m3ugen()
        else:
            print("Please login with options 1 or 2 before generating playlist")
    elif ch == 4:
        exit()
    else:
        print("Wrong input entered ... Exiting")
        exit(1)
