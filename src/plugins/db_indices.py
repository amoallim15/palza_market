import pymongo


async def main(app):
    # # notice indices..
    await app.db["notices"].create_index(
        [("title", pymongo.TEXT), ("content", pymongo.TEXT)]
    )
