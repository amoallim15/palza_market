from fastapi import Body
from src.models.wishlist import (
    PatchWishlistModel,
)


def main(app):
    @app.get("/wishlist/agency")
    def agencies():
        # TODO:
        pass

    @app.get("/wishlist/realstate")
    def realstates():
        # TODO:
        pass

    @app.patch("/wishlist/agency/{user_id}")
    def patch_agency_wishlist(user_id: str, wishlist: PatchWishlistModel = Body(...)):
        # TODO:
        pass

    @app.patch("/wishlist/realstate/{realstate_id}")
    def patch_realstate_wishlist(
        realstate_id: str, wishlist: PatchWishlistModel = Body(...)
    ):
        # TODO:
        pass
