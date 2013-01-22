import copy

from optparse import OptionParser
from pocketpy.auth import auth
from hncomments import utils

from pocketpy.pocket import retrieve, add
from pocketpy.tags import has_tag, remove_tags

def find_items_with_comments_tag(items):
    uids = []

    for uid, item in items.iteritems():
        if has_tag(item, "comments"):
            uids.append((uid, item.get('given_url', '')))

    return uids


def find_and_add_hn_urls(credentials, comment_items):
    config = copy.deepcopy(credentials)

    for uid, url in comment_items:
        hn_url = utils.get_hn_comments_url(url)
        if hn_url:
            config["url"] = hn_url
            add(config)
    uids = [uid for uid, url in comment_items]
    remove_tags(credentials, uids, ["comments"])


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('--key', dest='key',
        help='pocket apps consumer key')
    (options, args) = parser.parse_args()

    config = auth(options)
    credentials = copy.deepcopy(config)
    # retrieve items
    items = retrieve(config, verbose=True)

    comment_items = find_items_with_comments_tag(items)
    comment_urls = find_and_add_hn_urls(credentials, comment_items)
