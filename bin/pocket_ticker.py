import datetime
import os
import time

from pocketpy.auth import auth
from pocketpy.jsonconfig import JsonConfig
from pocketpy.pocket import retrieve


JSON_DIRECTORY = "pocket_json/"


if __name__ == "__main__":
    config = auth({})
    items = retrieve(config, verbose=True)
    timestamp = long(time.mktime(datetime.datetime.now().timetuple()))
    jc = JsonConfig(os.path.join(JSON_DIRECTORY, "%s.json" % str(timestamp)))
    jc.config = items
    jc.save(indent=4)
