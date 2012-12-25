import json
import sys
import requests

RETRIEVE_URL = "https://getpocket.com/v3/get"
SEND_URL = "https://getpocket.com/v3/send"


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
    if response.status_code != 200:
        print "Returned Status Code %d: %s" % (response.status_code,
        response.content)
        sys.exit(1)
    return response


def add_tags(config, item_ids, tags):
    actions = []

    for item_id in item_ids:
        action = {"action": "tags_add", "item_id": item_id, "tags": tags}
        actions.append(action)

    config["actions"] = actions
    response = modify(config)
    body = response.json()
    assert(body["status"] == 1)
