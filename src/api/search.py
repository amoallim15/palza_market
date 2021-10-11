# from src.models.api_models import Realstate
# from uuid import UUID


def main(app):
    @app.get("/search")
    def search(keyword: str, lng: int = 0, lat: int = 0, area: str = ""):
        # TODO:
        pass
