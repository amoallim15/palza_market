from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import (
    others,
    notice,
    realstate,
    report,
    user,
    home_page,
    review,
    search,
    image,
    sms,
    banner,
    wishlist,
    magazine,
    franchise,
    settings,
    callback,
)
from src.core import utils
from src.core.secret import Secret
from src.core.storage import MongoStore, ObjectStore
from src.plugins import authorization


# 1. initialize the server..
app = FastAPI(
    title="Palza Market",
    version="0.6.1",
    contact={
        "name": "Ali Moallim",
        "email": "moallim15@gmail.com",
    },
)

# 2. integrate initial configuration..
app.config = config = utils.get_config()
#
app.db = MongoStore(**config["DATABASE_CONFIG"]).connect()
app.s3 = ObjectStore(**config["IMAGE_STORE_CONFIG"]).connect()
app.secret = Secret(**config["SECRET"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=config["APP"]["origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 3. integrate plugins..
authorization.main(app, authentication_url="auth")


# 4. integrate routes..
user.main(app)
home_page.main(app)
settings.main(app)
realstate.main(app)
wishlist.main(app)
search.main(app)
review.main(app)
notice.main(app)
report.main(app)
banner.main(app)
magazine.main(app)
franchise.main(app)
image.main(app)
sms.main(app)
others.main(app)
callback.main(app)
