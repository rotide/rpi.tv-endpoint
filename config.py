import os
from pathlib import Path

basedir = os.path.abspath(os.path.dirname(__file__))
keyfile = os.path.join(basedir, 'key.txt')

def readKeyFile(file):
    key = None
    uuid = None
    if os.path.isfile(file):
        with open(file, 'r') as f:
            for line in f:
                if line [0:5] == 'uuid:':
                    uuid = line.split(':')[1].strip()
                elif line[0:4] == 'key:':
                    key = line.split(':')[1].strip()
    return uuid, key

class Config(object):
    KEYFILE = keyfile
    UUID, KEY = readKeyFile(KEYFILE)
    SERVER = '10.0.0.100'
    PORT = 5000
    NAME = "Test-LivingRoom"
