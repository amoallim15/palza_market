from fastapi import Body
from src.models.franchise import (
    CreateFranchiseModel,
    UpdateFranchiseModel,
)


def main(app):
    @app.get("/franchise")
    def franchises():
        # TODO:
        pass

    @app.get("/franchise/{franchise_id}")
    def get_franchise(franchise_id: str):
        # TODO:
        pass

    @app.post("/franchise")
    def create_franchise(franchise: CreateFranchiseModel = Body(...)):
        # TODO:
        pass

    @app.put("/franchise/{franchise_id}")
    def update_franchise(franchise_id: str, franchise: UpdateFranchiseModel = Body(...)):
        # TODO:
        pass

    @app.delete("/franchise/{franchise_id}")
    def delete_franchise(franchise_id: str):
        # TODO:
        pass
