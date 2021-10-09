from fastapi import FastAPI
from src.api import primary
from src.api import notice


# 1. initialize the server..
app = FastAPI()

# 2. integrate routes..
primary.main(app)
notice.main(app)
