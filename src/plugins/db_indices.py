import pymongo


async def main(app):
    # notice indices..
    await app.db["notices"].create_index(
        [("title", pymongo.TEXT), ("content", pymongo.TEXT)]
    )
    # realstate indices..
    await app.db["realstates"].create_index(
        [
            ("location", pymongo.GEOSPHERE),
        ]
    )
    await app.db["realstates"].create_index(
        [
            ("legal_address", pymongo.TEXT),
            ("title", pymongo.TEXT),
            ("m_name", pymongo.TEXT),
            ("s_name", pymongo.TEXT),
        ]
    )
    # pass
