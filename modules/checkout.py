import requests
import json

def checkout(server, port, uuid):
    url = 'http://' + str(server) + ':' + str(port) + '/api/endpoint/checkout/' + str(uuid)

    response = requests.get(url)
    response_json = response.json()

    if response.status_code == 200:
        #desired_state = response_json['desired_state']
        return response.status_code, response_json
    return response.status_code, None
