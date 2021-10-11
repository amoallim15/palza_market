# from src.models.api_models import *


def main(app):
    @app.get("/health")
    def health_check():
        return {"status": "OK"}
