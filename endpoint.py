import os, time
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

    errors = False

    while True:
        if time.time() - p.last_checkin_attempt >= delay:
            if p.checkin() and p.checkout():
                if errors:
                    print(' [*] Connection Established. Errors cleared.')
                    errors = False
            else:
                print(' [E] Communication Error. Trying again in %i seconds.' % delay)
                errors = True

            # If no errors, process checkin/checkout directives (play, stop, skip, etc)
            if not errors:
                p.process()

        # Slight delay to drop CPU usage
        time.sleep(.1)

if __name__ == '__main__':
    main()

# To get OMXPLAYER playing without permissions issues
# - echo 'SUBSYSTEM=="vchiq",GROUP="video",MODE="0660"' > /etc/udev/rules.d/10-vchiq-permissions.rules
# - usermod -a -G video YourUnprivilegedUser