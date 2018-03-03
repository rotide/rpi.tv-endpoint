import requests
import json

def checkin(server, port, name, uuid, key, state, channel, video):
    data = {'uuid':uuid, 'key':key, 'state':state, 'name':name, 'channel':channel, 'video':video}
    data_json = json.dumps(data)

    url = 'http://' + str(server) + ':' + str(port) + '/api/endpoint/checkin'
    headers = {'Content-type': 'application/json'}

    try:
        response = requests.post(url, data=data_json, headers=headers)
        return response.status_code
    except Exception as e:
        print('EXCEPTION: checkin(): %s' % str(e))
        return -1
