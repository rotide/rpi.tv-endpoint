import requests
import json

def register(server, port):
    url = 'http://' + str(server) + ':' + str(port) + '/api/endpoint/register'
    response = requests.post(url)
    data = response.json()
    if data['uuid'] and data['key']:
        #write_key(data, keyfile)
        return data
    return None

def writekey(json_data, keyfile):
    with open(keyfile, 'w+') as f:
        f.write('uuid:' + json_data['uuid'] + '\n')
        f.write('key:' + json_data['key'] + '\n')
