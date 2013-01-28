import os
import unittest

from mock import Mock, patch
from pocketpy.jsonconfig  import JsonConfig
from pocketpy.pocket  import retrieve, modify, add
from pocketpy.tags  import has_tag, tag_action

TEST_FILES_DIRECTORY = "pocketpy/test/test_files/"


class PocketTester(unittest.TestCase):
    def setUp(self):
        super(PocketTester, self).setUp()
        jc = JsonConfig(os.path.join(TEST_FILES_DIRECTORY, "sample.json"))
        items = jc.read()
        self.sample_items = {"list":items}

    def patch_requests(self, requests_get, status_code=200):
        requests_json = Mock()
        requests_json.json = lambda: self.sample_items
        requests_json.status_code = status_code
        if status_code != 200:
            requests_json.content = "Some error body"
        requests_get.return_value = requests_json
        return requests_get

    @patch("requests.get")
    def test_retrieve(self, requests_get):
        requests_get = self.patch_requests(requests_get)
        # config doesn't matter
        config = {}
        returned_items = retrieve(config)
        self.assertEquals(returned_items, self.sample_items["list"])

    @patch("requests.get")
    def test_retrieve_verbosity(self, requests_get):
        requests_get = self.patch_requests(requests_get)
        # config doesn't matter
        config = {}
        returned_items = retrieve(config, verbose=True)
        self.assertEquals(returned_items, self.sample_items["list"])

    @patch("requests.get")
    def test_retrieve_bad_request(self, requests_get):
        requests_get = self.patch_requests(requests_get, status_code=400)
        # config doesn't matter
        config = {}
        with self.assertRaises(SystemExit) as cm:
            returned_items = retrieve(config, verbose=True)

    @patch("requests.post")
    def test_modify_has_to_have_actions(self, requests_post):
        # config doesn't have actions
        config = {}
        with self.assertRaises(Exception) as cm:
            returned_items = modify(config)

        self.assertEquals(
                cm.exception.message, "Actions are not in the request body")

    @patch("requests.post")
    def test_modify_bad_request(self, requests_post):
        requests_post = self.patch_requests(requests_post, status_code=400)
        # config doesn't matter
        config = {"actions": ["something something"]}
        with self.assertRaises(SystemExit) as cm:
            modify(config)

    @patch("requests.post")
    def test_add_has_to_have_url(self, requests_post):
        # config doesn't have url
        config = {}
        with self.assertRaises(Exception) as cm:
            returned_items = add(config)

        self.assertEquals(
                cm.exception.message, '"url" is not in the request body')

    @patch("requests.post")
    def test_add_bad_request(self, requests_post):
        requests_post = self.patch_requests(requests_post, status_code=400)
        # config doesn't matter
        config = {"url": "this doesnt matter"}
        with self.assertRaises(SystemExit) as cm:
            add(config)

    def test_has_tags(self):
        # no tags in item is false.
        self.assertFalse(has_tag({}, "sometag"))
        # tag in item
        self.assertTrue(has_tag({"tags": {"sometag": 1}}, "sometag"))
        # tag not in item
        self.assertFalse(has_tag({"tags": {"anothertag": 1}}, "sometag"))

    @patch("pocketpy.tags.modify")
    def test_tag_action(self, pocket_modify):
        response_mock = Mock()
        response_mock.json = lambda: {"status": 1}
        pocket_modify.return_value = response_mock
        # config doesn't matter
        tags = ["this", "tags", "needz", "adding"]
        item_ids = range(0, 100)
        action = "tags_add"
        config = {}
        tag_action(config, item_ids, tags, action)
        self.assertEquals(config["actions"],
            [ {"action": action, "item_id": item_id, "tags": tags}
                for item_id in item_ids])


if __name__ == "__main__":
	unittest.main()
