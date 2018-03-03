import requests
import json

def checkout(server, port, uuid):
    url = 'http://' + str(server) + ':' + str(port) + '/api/endpoint/checkout/' + str(uuid)

    try:
        response = requests.get(url)
        response_json = response.json()

        if response.status_code == 200:
            return response.status_code, response_json
        return response.status_code, None
    except Exception as e:
        print('EXCEPTION: checkout(): %s' % str(e))
        return -1