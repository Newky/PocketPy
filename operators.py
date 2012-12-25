import copy

from optparse import OptionParser
from auth import auth
from pocket import retrieve, add_tags


def has_long_tag(item):
    return has_tag(item, 'long')


def has_tag(item, tag):
    if "tags" not in item:
        return False
    else:
        if tag not in item["tags"].keys():
            return False
        else:
            return True

def isolate_long_articles(items, long_word_count=5000):
    uids = []

    for uid, item in items.iteritems():
        # get a word count from each item
        word_count = item.get('word_count', None)
        if not word_count:
            continue
        word_count = long(word_count)
        # if the word count is above the long word count
        if word_count > long_word_count:
            if not has_long_tag(item):
                uids.append(uid)

    return uids


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('--key', dest='key',
        help='pocket apps consumer key')
    (options, args) = parser.parse_args()

    config = auth(options)
    credentials = copy.deepcopy(config)
    items = retrieve(config, verbose=True)
    uids = isolate_long_articles(items)

    if len(uids) > 0:
        add_tags(credentials, uids, ["long"])
