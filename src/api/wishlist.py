from fastapi import Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from src.core.model import ListModel
from src.core.enums import UserType

from src.models.wishlist import (
    WishlistModel,
    PatchWishlistModel,
)


def main(app):
    @app.get("/wishlist/agency", response_model=ListModel)
    async def agencies(
        page: int = Query(0, ge=0),
        current_user=Depends(app.current_user),
        page_size: int = 10,
    ):
        data_list = []
        count = 0
        #
        data = app.db["wishlists"].find_one({"user_id": str(current_user.id)})
        #
        if data is not None:
            count = len(data["agency_ids"])
            data_list = data["agency_ids"][
                page * page_size : page_size + (page * page_size) + (page * page_size)
            ]
        #
        result = {
            "data": data_list,
            "info": {"count": count, "page": page, "page_size": page_size},
        }
        return ListModel(**result)

    @app.get("/wishlist/realstate", response_model=ListModel)
    async def realstates(
        page: int = Query(0, ge=0),
        current_user=Depends(app.current_user),
        page_size: int = 10,
    ):
        data_list = []
        count = 0
        #
        data = app.db["wishlists"].find_one({"user_id": str(current_user.id)})
        #
        if data is not None:
            count = len(data["realstate_ids"])
            data_list = data["realstate_ids"][
                page * page_size : page_size + (page * page_size) + (page * page_size)
            ]
        #
        result = {
            "data": data_list,
            "info": {"count": count, "page": page, "page_size": page_size},
        }
        return ListModel(**result)

    @app.patch("/wishlist", response_model=WishlistModel)
    async def patch_agency_wishlist(
        wishlist: PatchWishlistModel = Body(...), current_user=Depends(app.current_user)
    ):
        if current_user.user_type != UserType.INDIVIDUAL:
            raise HTTPException(status_code=403, detail="Not allowed.")

        data = await app.db["wishlists"].find_one({"user_id": str(current_user.id)})
        if not data:
            data = WishlistModel(user_id=str(current_user.id))
            data = jsonable_encoder(data)
            await app.db["wishlists"].insert_one(data)
        data = WishlistModel(**data)
        #
        if wishlist.operation:
            data.realstate_ids = list(set(data.realstate_ids + wishlist.realstate_ids))
            data.agency_ids = list(set(data.agency_ids + wishlist.agency_ids))
        else:
            data.realstate_ids = list(
                set(data.realstate_ids) - set(wishlist.realstate_ids)
            )
            data.agency_ids = list(set(data.agency_ids) - set(wishlist.agency_ids))
        #
        wishlist = jsonable_encoder(data)
        #
        await app.db["wishlists"].update_one(
            {"user_id": str(current_user.id)}, {"$set": wishlist}
        )
        data = await app.db["wishlists"].find_one({"user_id": str(current_user.id)})
        if data is None:
            raise HTTPException(status_code=404, detail="Wishlist not found.")
        #
        return WishlistModel(**data)
