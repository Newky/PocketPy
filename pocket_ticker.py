import datetime
import os
import time


from auth import auth
from jsonconfig import JsonConfig
from pocket import retrieve


JSON_DIRECTORY = "pocket_json/"


if __name__ == "__main__":
    config = auth({})
    items = retrieve(config, verbose=True)
    timestamp = long(time.mktime(datetime.datetime.now().timetuple()))
    jc = JsonConfig(os.path.join(JSON_DIRECTORY, "%s.json" % str(timestamp)))
    jc.config = items
    jc.save(indent=4)
