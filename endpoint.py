import time
from modules.player import Player
from config import Config

def main():
    p = Player(Config)
    delay = 3

    # Verifiy this device appears to be registered with the server.
    p.reg_check()

    # Print basic device information.
    print(' [*] Device UUID: ' + p.uuid)
    print(' [*] Device Name: ' + p.name)

    connected = False
    checkin_pass = True
    checkout_pass = True

    while True:
        if time.time() - p.last_checkin >= delay:
            try:
                p.checkin()
                checkin_pass = True
            except:
                if checkin_pass:
                    print(' [*] Communication Error: Checkin')
                    checkin_pass = False

            try:
                #p.statecheck()
                p.checkout()
                checkout_pass = True
            except:
                if checkout_pass:
                    print(' [*] Communication Error: Checkout')
                    checkout_pass = False

            if not connected:
                if checkin_pass and checkout_pass:
                    print(' [*] Connected')
                    connected = True
                else:
                    time.sleep(5)
            else:
                if not checkin_pass or not checkout_pass:
                    connected = False




        time.sleep(.1)

        #player = subprocess.Popen(['omxplayer', '-b', '-o', 'hdmi', <video>, '>', '/dev/null', '2>&1'])

if __name__ == '__main__':
    main()
