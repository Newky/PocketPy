import copy
import re

from optparse import OptionParser
from auth import auth
from jsonconfig import JsonConfig
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


def isolate_keyword_articles(items, kword, kword_tag):
    uids = []
    for uid, item in items.iteritems():
        # get a word count from each item
        title = item.get('resolved_title', None)
        if not title:
            continue
        word_exp = re.compile(r'\b%s\b' % kword, flags=re.IGNORECASE)
        match = word_exp.search(title.lower())
        if match:
            if not has_tag(item, kword_tag):
                uids.append(uid)

    return uids


def tag_long_articles(credentials, items):
    uids = isolate_long_articles(items)
    add_tags(credentials, uids, ["long"])
    return len(uids)


def tag_kword_articles(credentials, items):
    jc = JsonConfig(".kwords")
    config = jc.read()
    kwords = config["keywords"]
    total_uids = []
    for kword, kword_tag in kwords:
        uids = isolate_keyword_articles(items, kword.lower(), kword_tag)
        add_tags(credentials, uids, [kword_tag])
        total_uids.extend(uids)

    return len(total_uids)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('--key', dest='key',
        help='pocket apps consumer key')
    parser.add_option('--longs', dest='longs', action='store_true',
        default=False, help='tag untagged long articles')
    parser.add_option('--kwords', dest='kwords', action='store_true',
        default=False, help='tag untagged keyword articles')
    (options, args) = parser.parse_args()

    config = auth(options)
    credentials = copy.deepcopy(config)
    items = retrieve(config, verbose=True)

    if options.longs:
        affected = tag_long_articles(credentials, items)
        print "Tagged %d long articles" % (affected)

    if options.kwords:
        affected = tag_kword_articles(credentials, items)
        print "Tagged %d kword articles" % (affected)
