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

        if p.is_playing():
            p.stop()
        else:
            p.play('/home/rotide/media/tv/mtv/Young.Sheldon.S01E01.720p.HDTV.X264-DIMENSION.mkv')

if __name__ == '__main__':
    main()
