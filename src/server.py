from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import (
    auth,
    user,
    settings,
    image,
    notice,
    notice_category,
    franchise,
    magazine,
    crontab,
    others,
    banner,
    sms,
    report,
    review,
    wishlist,
    realstate,
    search,
    callbacks,
)
from src.core import utils
from src.core.secret import Secret
from src.core.storage import MongoStore, ObjectStore
from src.plugins import authorization, db_indices


# 1. initialize the server..
config = utils.get_config()
app = FastAPI(
    title="Palza Market",
    version="0.6.1",
    contact={
        "name": "Ali Moallim",
        "email": "moallim15@gmail.com",
    },
)
db = MongoStore(**config["DATABASE_CONFIG"])
s3 = ObjectStore(**config["IMAGE_STORE_CONFIG"])
secret = Secret(**config["SECRET"])


async def startup():
    app.config = config = utils.get_config()
    #
    app.db = await db.connect()
    app.s3 = await s3.connect()
    app.secret = Secret(**config["SECRET"])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config["CORS"]["origins"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # integrate async plugins..
    await db_indices.main(app)


async def shutdown():
    await db.close()
    await s3.close()


#

# 2. add event handlers..
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

# 3. integrate plugins..
authorization.main(app, authentication_url="auth")

# 4. integrate routes..
others.main(app)
auth.main(app)
user.main(app)
settings.main(app)
image.main(app)
notice.main(app)
notice_category.main(app)
franchise.main(app)
magazine.main(app)
crontab.main(app)
banner.main(app)
sms.main(app)
report.main(app)
review.main(app)
wishlist.main(app)
realstate.main(app)
search.main(app)
callbacks.main(app)
