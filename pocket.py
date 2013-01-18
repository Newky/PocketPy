import json
import sys
import requests

RETRIEVE_URL = "https://getpocket.com/v3/get"
SEND_URL = "https://getpocket.com/v3/send"
ADD_URL = "https://getpocket.com/v3/add"


def retrieve(config, verbose=False):
    if verbose:
        config["detailType"] = 'complete'
    response = requests.get(RETRIEVE_URL, params=config)
    items = response.json()['list']
    return items


def modify(config):
    if 'actions' not in config:
        raise Exception('Actions are not in the request body')
    headers = {'content-type': 'application/json',
        'X-Accept': 'application/json'}
    payload = json.dumps(config)
    response = requests.post(SEND_URL, headers=headers, data=payload)
    if response.status_code not in range(200, 299):
        print "Returned Status Code %d: %s" % (response.status_code,
        response.content)
        sys.exit(1)
    return response

def add(config):
    if 'url' not in config:
        raise Exception('"url" is not in the request body')
    headers = {'content-type': 'application/json',
        'X-Accept': 'application/json'}
    payload = json.dumps(config)
    response = requests.post(ADD_URL, headers=headers, data=payload)
    if response.status_code != 200:
        print "Returned Status Code %d: %s" % (response.status_code,
        response.content)
        sys.exit(1)
    return response
