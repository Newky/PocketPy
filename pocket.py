import json
import sys

from optparse import OptionParser

import requests

from auth import auth

RETRIEVE_URL = "https://getpocket.com/v3/get"


def retrieve(config):
    response = requests.get(RETRIEVE_URL, params=config)
    items = response.json()['list']
    return items

def simple_explore(items):
    for key, item in items.iteritems():
        explore(item)


def explore(item):
    linefeed = raw_input("Enter n to continue to next item:")
    while linefeed != 'n':
        if linefeed == 'keys':
            print item.keys()
        else:
            if linefeed in item:
                print item[linefeed]
        linefeed = raw_input("Enter n to continue to next item:")


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('--key', dest='key',
        help='pocket apps consumer key')
    (options, args) = parser.parse_args()

    config = auth(options)
    items = retrieve(config)
    simple_explore(items)
