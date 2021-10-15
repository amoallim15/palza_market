from fastapi import FastAPI
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
)
from src.core import utils
from src.core.storage import MongoStore, ObjectStore
from src.plugins import authorization


# 1. initialize the server..
app = FastAPI(
    title="Palza Market",
    version="0.4.12",
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

# 3. integrate plugins..
authorization.main(app, authentication_url="auth")

# 4. integrate routes..
user.main(app)
home_page.main(app)
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
