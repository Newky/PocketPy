from pocket import modify


def tag_action(config, item_ids, tags, action):
    if len(item_ids) <= 0:
        return
    actions = []

    for item_id in item_ids:
        action_obj = {"action": action, "item_id": item_id, "tags": tags}
        actions.append(action_obj)

    config["actions"] = actions
    response = modify(config)
    body = response.json()
    assert(body["status"] == 1)


def add_tags(config, item_ids, tags):
    tag_action(config, item_ids, tags, "tags_add")


def remove_tags(config, item_ids, tags):
    tag_action(config, item_ids, tags, "tags_remove")


def has_tag(item, tag):
    if "tags" not in item:
        return False
    else:
        if tag not in item["tags"].keys():
            return False
        else:
            return True
