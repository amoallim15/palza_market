from fastapi import Body
from src.models.banner import (
    CreateBannerModel,
    UpdateBannerModel,
)


def main(app):
    @app.get("/banner")
    def banners():
        # TODO:
        pass

    @app.get("/banner/{banner_id}")
    def get_banner(banner_id: str):
        # TODO:
        pass

    @app.post("/user")
    def create_user(user: CreateBannerModel = Body(...)):
        # TODO:
        pass

    @app.put("/banner/{banner_id}")
    def update_banner(banner_id: str, banner: UpdateBannerModel = Body(...)):
        # TODO:
        pass

    @app.delete("/banner/{banner_id}")
    def delete_banner(banner_id: str):
        # TODO:
        pass
