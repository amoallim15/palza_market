from fastapi import Body
from src.models.magazine import (
    CreateMagazineModel,
    UpdateMagazineModel,
)


def main(app):
    @app.get("/magazine")
    def magazines():
        # TODO:
        pass

    @app.get("/magazine/{magazine_id}")
    def get_magazine(magazine_id: str):
        # TODO:
        pass

    @app.post("/magazine")
    def create_magazine(magazine: CreateMagazineModel = Body(...)):
        # TODO:
        pass

    @app.put("/magazine/{magazine_id}")
    def update_magazine(magazine_id: str, magazine: UpdateMagazineModel = Body(...)):
        # TODO:
        pass

    @app.delete("/magazine/{magazine_id}")
    def delete_magazine(magazine_id: str):
        # TODO:
        pass
