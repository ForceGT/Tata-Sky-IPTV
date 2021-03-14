import login

while True :
    print("Welcome To TataSky Channel Generation Script")
    print("#############################################")
    print("Using this script you can generate playable links based on the channels you have subscribed to \n This can also generate a m3u playlist based on your choice selection \n [Coming SOON] Support for generating links directly based on channel id ")
    print("Menu:")
    print("1. Login using SID")
    print("2. Login using RMN")
    print("3. Generate my playlist")
    ch = int(input("Enter your choice:"))
    print(ch)
    if ch == 1:
        sid = str(input("Enter your subId:"))
        print("1. Login with password")
        print("2. Login with OTP")
        ch2 = int(input("Enter your choice:"))
        if ch2 == 1:
            pwd = str(input("Enter your password:"))
            login.loginWithPass(sid=sid, rmn="", pwd=pwd)
            break
        elif ch2 == 2:
            login.generateOTP(sid=sid, rmn="")
            otp = str(input("Enter the OTP sent to your rmn"))
            login.loginWithOTP(sid=sid, rmn="", otp=otp)
        else:
            print("Wrong input entered.. Exiting")
            exit(1)
    elif ch == 2:
        rmn = str(input("Enter your RMN"))
        print("1. Login with password")
        print("2. Login with OTP")
        ch2 = int(input("Enter your choice:"))
        if ch2 == 1:
            pwd = str(input("Enter your password:"))
            login.loginWithPass(sid=sid, rmn="", pwd=pwd)
        elif ch2 == 2:
            login.generateOTP(sid=sid, rmn="")
            otp = str(input("Enter the OTP sent to your rmn"))
            login.loginWithOTP(sid=sid, rmn="", otp=otp)
        else:
            print("Wrong input entered...Exiting")
            exit(1)
    else:
        print("Wrong input entered ... Exiting")
        exit(1)