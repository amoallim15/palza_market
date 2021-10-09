# from src.models.api_models import *


def main(app):
    @app.get("/")
    def index():
        return { "status": "OK" }
