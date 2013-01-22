import requests
import sys

from optparse import OptionParser

from jsonconfig import JsonConfig


AUTH_URL = ("https://getpocket.com/auth/authorize?"
        "request_token=%s&redirect_uri=%s")
REQUEST_TOKEN_URL = "https://getpocket.com/v3/oauth/request"
AUTH_TOKEN_URL = "https://getpocket.com/v3/oauth/authorize"
REDIRECT_URL = "http://www.richydelaney.com/success/"
CONFIG_FILE = '.creds'


def auth(options):
    jc = JsonConfig(CONFIG_FILE)
    access_token = None
    if getattr(options, "key", False):
        consumer_key = options.key
    else:
        consumer_key, access_token = get_credentials_from_config(jc.read())

    if not consumer_key:
        print "Need to provide a consumer key using the .creds config file"
        print "Or by using the --key command line argument."
        sys.exit(1)

    if not access_token:
        access_token, username = access_token_flow(consumer_key)

    jc.config = {'consumer_key': consumer_key, 'access_token': access_token}
    jc.save()
    return jc.read()


def access_token_flow(consumer_key):
    code = get_authentication_token(consumer_key)
    redirect_user(code)
    return get_access_token(consumer_key, code)


def get_authentication_token(consumer_key):
    payload = {'consumer_key': consumer_key,
        'redirect_uri': REDIRECT_URL}
    headers = {'X-Accept': 'application/json'}
    response = requests.post(REQUEST_TOKEN_URL, data=payload, headers=headers)
    if response.status_code != 200:
        print "Returned Status Code %d: %s" % (response.status_code,
        response.content)
        sys.exit(1)
    body = response.json()
    return body["code"]


def redirect_user(code):
    print "please go the following website and authenticate:"
    print AUTH_URL % (code, REDIRECT_URL)
    raw_input("When you have completed, press enter:")


def get_access_token(consumer_key, code):
    payload = {'consumer_key': consumer_key,
        'code': code}
    headers = {'X-Accept': 'application/json'}
    response = requests.post(AUTH_TOKEN_URL, data=payload, headers=headers)
    body = response.json()
    return body["access_token"], body["username"]


def get_credentials_from_config(config):
    return (config.get('consumer_key', None),
        config.get('access_token', None))


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('--key', dest='key',
        help='pocket apps consumer key')
    (options, args) = parser.parse_args()

    auth(options)
