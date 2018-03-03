import os, time, sys, subprocess
from modules.registration import register, writekey
from modules.checkin import checkin
from modules.checkout import checkout

class Player(object):
    # Basic Settings
    server = None
    port = None
    keyfile = None

    # Identification/Authorization
    uuid = None
    key = None
    name = None

    # Player States: STOPPED, PLAYING, PAUSED, ERROR
    # Current state of the player.
    player_state = 'STOPPED'
    # Desired States: STOP, PLAY, PAUSE
    # Desired state of the player (remote control)
    desired_state = None
    desired_channel = None
    queued_video = None

    # Epoch of last checkin attempt
    last_checkin_attempt = None

    # Variable to hold Video Player object
    player = None

    def __init__(self, Config):
        self.server = Config.SERVER
        self.port = Config.PORT
        self.name = Config.NAME
        self.uuid = Config.UUID
        self.key = Config.KEY
        self.keyfile = Config.KEYFILE
        self.last_checkin_attempt = 0

    def is_playing(self):
        if self.player is not None and self.player.poll() is None:
            # Video is playing (poll() returned no exit code)
            return True
        else:
            return False

    def play(self, v):
        # Original subprocess creation from OLD script.
        # - self.player = subprocess.Popen(['omxplayer', '-b', '-o', 'hdmi', v, '>', '/dev/null', '2>&1'])
        self.player = subprocess.Popen(['omxplayer', '-b', '-o', 'hdmi', v, '>', '/dev/null', '2>&1'], shell=False)
        print('Spawned PID: ' + str(self.player.pid))

    def pause(self):
        if self.is_playing():
            stdout, stderror = self.player.communicate(input='p')
            print(stdout)
            print(stderror)

    def stop(self):
        if self.is_playing()
            os.system('killall -9 omxplayer')
            os.system('killall -9 omxplayer.bin')
            self.player_state = 'STOP'
            self.player = None

    def reg_check(self):
        if self.uuid == None or self.key == None:
            print(' [*] Registration appears to be incomplete')
            print('  -  Registering device with server')
            success = self.register()
            if not success:
                print(' [*] Registration Failed, please edit config.py')
                sys.exit(1)
            print(' [*] Registration Successful!')
        else:
            print(' [*] Device appears to be registered')

    def register(self):
        result = register(self.server, self.port)
        if result:
            self.uuid = result['uuid']
            self.key = result['key']
            writekey(result, self.keyfile)
            return True
        return False

    def checkin(self):
        self.last_checkin_attempt = time.time()

        status_code = checkin(self.server, self.port, self.name,
                              self.uuid, self.key, self.player_state,
                              self.desired_channel, self.queued_video)

        if status_code is 202:
            return True
        else:
            print(' [E] Checkin Failed: %i' % int(status_code))
            return False

    def checkout(self):
        status_code, state_json = checkout(self.server,
                                           self.port,
                                           self.uuid)

        if int(status_code) == 200:
            d_s = state_json[self.uuid]['desired_state']
            d_c = state_json[self.uuid]['desired_channel']
            q_v = state_json[self.uuid]['queued_video']

            # Check Desired State - Set if changed
            if self.desired_state != d_s:
                print(' [i] State Change: %s -> %s' %(str(self.desired_state),
                                                      str(d_s)))
                self.desired_state = d_s

            # Check Desired Channel - Set if changed
            if self.desired_channel != d_c:
                print(' [i] Channel Change: %s -> %s' %(str(self.desired_channel),
                                                        str(d_c)))
                self.desired_channel = d_c

            # Check Queued Video - Set if changed
            if self.queued_video != q_v:
                print(' [i] Queued Video Change: %s -> %s' %(str(self.queued_video),
                                                             str(q_v)))
                self.queued_video = q_v
            return True
        else:
            print(' [E] Checkout Failed: %i' % int(status_code))
            return False