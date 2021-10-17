def main(config, settings, db):
    result = []
    # 1. get business nums..
    business_nums = {}
    businesses = db["realstates"].find({"business_no": {"$ne": None}})
    pass
