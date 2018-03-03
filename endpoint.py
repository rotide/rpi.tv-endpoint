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

        time.sleep(.1)

        if not p.is_playing() and p.desired_state == 'PLAY':
            p.play('/mnt/media/tv/mtv/Young.Sheldon.S01E01.720p.HDTV.X264-DIMENSION.mkv')
        if p.desired_state == 'STOP' and p.is_playing():
            p.stop()

if __name__ == '__main__':
    main()
