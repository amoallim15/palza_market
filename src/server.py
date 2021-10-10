from fastapi import FastAPI
from src.api import primary
from src.api import notice
from src.core import utils

# 1. import config
config = utils.get_config()

# 2. initialize the server..
app = FastAPI()

# 3. integrate routes..
primary.main(app)
notice.main(app)
