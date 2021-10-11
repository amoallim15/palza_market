from fastapi import FastAPI
from src.api import (
    others,
    notice,
    realstate,
    report,
    auth,
    home_page,
    review,
    search,
    image,
    sms,
)
from src.core import utils

# 1. import config..
config = utils.get_config()

# 2. initialize the server..
app = FastAPI(
    title="Palza Market",
    version="0.4.7",
    contact={
        "name": "Ali Moallim",
        "email": "moallim15@gmail.com",
    }
)

# 3. integrate routes..
auth.main(app)
home_page.main(app)
realstate.main(app)
search.main(app)
review.main(app)
notice.main(app)
report.main(app)
image.main(app)
sms.main(app)
others.main(app)
