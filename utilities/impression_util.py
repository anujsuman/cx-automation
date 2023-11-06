import json


def parse_impressions(data):
    all_imps = []

    if data and "requests" in data and len(data["requests"]) == 0:
        return all_imps

    for request in data.get("requests", []):
        if "add-impression" in request.get("url", ""):
            body = request.get("body", "")
            try:
                impressions = json.loads(body).get("impressions", [])
                all_imps.extend(impressions)
            except json.JSONDecodeError:
                pass
    return all_imps


def filter_unique_ranks(impressions):
    unique_ranks = set()
    filtered_impressions = []

    for impression in impressions:
        vertical_rank = impression.get("vertical_rank")
        horizontal_rank = impression.get("horizontal_rank")

        # Check if the combination of vertical_rank and horizontal_rank is unique
        rank_key = (vertical_rank, horizontal_rank)

        if rank_key not in unique_ranks:
            unique_ranks.add(rank_key)
            filtered_impressions.append(impression)

    return filtered_impressions


def generate_impressions_lookup(impression_data):
    impressions_lookup = {}
    for impression in impression_data:
        asset_id = impression.get("asset_id")
        asset_type = impression.get("asset_type")
        vertical_rank = impression.get("vertical_rank")
        horizontal_rank = impression.get("horizontal_rank")
        screen_name = impression.get("screen_name")
        action = impression.get("action")
        cms_page_id = impression.get("cms_page_id")
        asset_parent_id = impression.get("asset_parent_id")
        asset_parent_type = impression.get("asset_parent_type")

        key = (asset_id, asset_type, vertical_rank, horizontal_rank, screen_name, action, cms_page_id, asset_parent_id,
               asset_parent_type)

        # key = (cms_item_id, vertical_rank, horizontal_rank)

        impressions_lookup[key] = impression

    return impressions_lookup


def generate_impressions_assetId_parent_id_lookup(impression_data):
    impressions_lookup = {}
    for impression in impression_data:
        asset_id = impression.get("asset_id")
        screen_name = impression.get("screen_name")
        asset_parent_id = impression.get("asset_parent_id")

        key = (asset_id, asset_parent_id, screen_name)

        # key = (cms_item_id, vertical_rank, horizontal_rank)

        impressions_lookup[key] = impression

    return impressions_lookup


def get_max_vertical_rank(data):
    max_rank = 0

    for item in data["data"]["list_items"]:
        vertical_rank = item.get("vertical_rank")
        if vertical_rank > max_rank:
            max_rank = vertical_rank

        if "list_items" in item:
            for sub_item in item["list_items"]:
                sub_vertical_rank = sub_item.get("vertical_rank")
                if sub_vertical_rank > max_rank:
                    max_rank = sub_vertical_rank

        if "products" in item:
            for sub_item in item["products"]:
                sub_vertical_rank = sub_item.get("vertical_rank")
                if sub_vertical_rank > max_rank:
                    max_rank = sub_vertical_rank

    return max_rank


def assign_ranks_cms(data, is_cms_item_parsing=False, vertical_rank=1):
    cms_page_id = data["data"]["cms_item_id"]
    cms_page_type = data["data"]["type"]
    screen_name = 'Home'
    action = 'IMPRESSION'

    if is_cms_item_parsing:
        screen_name = 'DynamicCMSListing'

    for item in data["data"]["list_items"]:
        item["asset_id"] = item["cms_item_id"]
        item["asset_type"] = item["type"]
        item["vertical_rank"] = vertical_rank
        item["screen_name"] = screen_name
        item["action"] = action
        item["cms_page_id"] = cms_page_id
        item["asset_parent_id"] = cms_page_id
        item["asset_parent_type"] = cms_page_type

        horizontal_rank = 1

        if "list_items" in item:
            list_items = []
            for sub_item in item["list_items"]:
                sub_item["asset_id"] = sub_item["cms_item_id"]
                sub_item["asset_type"] = sub_item["type"]
                sub_item["vertical_rank"] = vertical_rank
                sub_item["horizontal_rank"] = horizontal_rank
                sub_item["screen_name"] = screen_name
                sub_item["action"] = action
                sub_item["cms_page_id"] = cms_page_id
                sub_item["asset_parent_id"] = item["cms_item_id"]
                sub_item["asset_parent_type"] = item["type"]

                list_items.append(sub_item)
                horizontal_rank += 1
            item["list_items"] = list_items

        horizontal_rank = 1

        if "products" in item:
            products = []
            for sub_item in item["products"]:
                sub_item["asset_id"] = sub_item["sku_id"]
                sub_item["asset_type"] = "SKU"
                sub_item["vertical_rank"] = vertical_rank
                sub_item["horizontal_rank"] = horizontal_rank
                sub_item["screen_name"] = screen_name
                sub_item["action"] = action
                sub_item["cms_page_id"] = cms_page_id
                sub_item["asset_parent_id"] = item["cms_item_id"]
                sub_item["asset_parent_type"] = item["type"]

                products.append(sub_item)
                horizontal_rank += 1
            item["products"] = products

        else:
            item["horizontal_rank"] = 1

        vertical_rank += 1


def re_assign_ranks_cms(prev_cms_data, new_cms_data):
    max_vertical_rank = get_max_vertical_rank(prev_cms_data)
    assign_ranks_cms(new_cms_data, False, max_vertical_rank + 1)


def assign_ranks_items(data, cms_home_data=False):
    vertical_rank = 1
    cms_page_id = data["data"]["cms_item_id"]
    cms_page_type = 'home_list'
    screen_name = 'DynamicCMSListing'

    if cms_home_data:
        screen_name = 'Home'

    action = 'IMPRESSION'

    for item in data["data"]["products"]:
        item["asset_id"] = item["sku_id"]
        item["asset_type"] = "SKU"
        item["vertical_rank"] = vertical_rank
        item["horizontal_rank"] = None
        item["screen_name"] = screen_name
        item["action"] = action
        item["cms_page_id"] = cms_page_id
        item["asset_parent_id"] = cms_page_id
        item["asset_parent_type"] = cms_page_type

        vertical_rank += 1


def assign_ranks_yml_items(data):
    horizontal_rank = 1
    asset_parent_id = data["data"]["cms_item_id"]
    cms_page_id = ''
    cms_page_type = 'YOU_MAY_ALSO_LIKE_PDU'
    screen_name = 'DynamicCMSListing'
    action = 'IMPRESSION'

    for item in data["data"].get("products", []):
        item["asset_id"] = item["sku_id"]
        item["asset_type"] = "SKU"
        item["vertical_rank"] = None
        item["horizontal_rank"] = horizontal_rank
        item["screen_name"] = screen_name
        item["action"] = action
        item["cms_page_id"] = cms_page_id
        item["asset_parent_id"] = asset_parent_id
        item["asset_parent_type"] = cms_page_type

        horizontal_rank += 1
