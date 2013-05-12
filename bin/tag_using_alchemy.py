import copy
import requests

from urllib import quote_plus
from optparse import OptionParser

from pocketpy.auth import auth
from pocketpy.pocket import retrieve

KEYWORD_URL = "http://access.alchemyapi.com/calls/url/URLGetRankedKeywords"


def get_keywords_from_alchemy(access_token, item_url):
    params = {"url": item_url, "apikey": access_token,
            "maxRetrieve": 5, "outputMode": "json"}
    response = requests.get(KEYWORD_URL, params=params)
    body = response.json()
    keywords = []
    if body.get("keywords", None):
        for keyword in body["keywords"]:
            if float(keyword["relevance"]) > 0.9:
                keywords.append(keyword["text"])
    return keywords

def tag_items_if_not_already_tagged(credentials, items, access_token,
        dry_run=True):
    for uid, item in items.iteritems():
        item_url = item.get("resolved_url")
        keywords = get_keywords_from_alchemy(access_token, item_url)
        if dry_run:
            print item_url, keywords
        else:
            if "tags" not in item:
                add_tags(credentials, uid, [tags])


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('--alchemy-key', dest='alchemy_key',
            help='alchemy access token')
    parser.add_option('--dry-run', dest='dryrun', action='store_true',
            default=False, help='Enable for a dry run')
    (options, args) = parser.parse_args()

    config = auth(options)
    credentials = copy.deepcopy(config)
    items = retrieve(config, verbose=True)

    tag_items_if_not_already_tagged(credentials, items, options.alchemy_key,
            dry_run=options.dryrun)
