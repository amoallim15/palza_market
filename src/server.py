from fastapi import FastAPI
from src.api import (
    primary,
    notice,
    realstate,
    report,
    auth,
    home_page,
    review,
    search,
    image,
)
from src.core import utils

# 1. import config..
config = utils.get_config()

# 2. initialize the server..
app = FastAPI()

# 3. integrate routes..
primary.main(app)
notice.main(app)
realstate.main(app)
report.main(app)
auth.main(app)
home_page.main(app)
review.main(app)
search.main(app)
image.main(app)
