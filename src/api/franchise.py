from fastapi import Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from src.core.utils import update_image, short_uuid
from src.core.model import ListModel, SuccessModel
from src.core.enums import UserRole

from src.models.franchise import (
    FranchiseModel,
    CreateFranchiseModel,
    UpdateFranchiseModel,
)


def main(app):
    @app.get("/franchise", response_model=ListModel)
    async def franchises(page: int = Query(0, ge=0), page_size: int = 10):
        pipeline = [
            {"$sort": {"_id": -1}},
            {
                "$facet": {
                    "data": [{"$skip": page * page_size}, {"$limit": page_size}],
                    "info": [
                        {"$count": "count"},
                        {"$addFields": {"page": page}},
                        {"$addFields": {"page_size": page_size}},
                    ],
                }
            },
            {"$unwind": "$info"},
        ]
        #
        try:
            result = await app.db["franchises"].aggregate(pipeline).next()
        except StopAsyncIteration:
            result = {"info": {"count": 0, "page": page, "page_size": page_size}}
        return ListModel(**result)

    @app.get("/franchise/{franchise_id}", response_model=FranchiseModel)
    async def get_franchise(franchise_id: str):
        data = await app.db["franchises"].find_one({"_id": franchise_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Franchise not found.")
        #
        return FranchiseModel(**data)

    @app.post("/franchise", response_model=FranchiseModel)
    async def create_franchise(
        franchise: CreateFranchiseModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        franchise.thumbnail_url = update_image(
            app=app,
            old_path=franchise.thumbnail_url,
            new_path=f"franchises/{franchise.id}",
            name=f"{short_uuid()}-thumbnail",
        )
        #
        franchise = jsonable_encoder(franchise)
        #
        result = await app.db["franchises"].insert_one(franchise)
        data = await app.db["franchises"].find_one({"_id": result.inserted_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Franchise not found.")
        #
        return FranchiseModel(**data)

    @app.put("/franchise/{franchise_id}", response_model=FranchiseModel)
    async def update_franchise(
        franchise_id: str,
        franchise: UpdateFranchiseModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        if "tmp" in franchise.thumbnail_url:
            franchise.thumbnail_url = update_image(
                app=app,
                old_path=franchise.thumbnail_url,
                new_path=f"franchises/{franchise_id}",
                name=f"{short_uuid()}-thumbnail",
            )
        #
        franchise = jsonable_encoder(franchise)
        #
        await app.db["franchises"].update_one(
            {"_id": franchise_id}, {"$set": franchise}
        )
        data = await app.db["franchises"].find_one({"_id": franchise_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Franchise not found.")
        #
        return FranchiseModel(**data)

    @app.delete("/franchise/{franchise_id}", response_model=SuccessModel)
    async def delete_franchise(
        franchise_id: str, current_user=Depends(app.current_user)
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        result = await app.db["franchises"].delete_one({"_id": franchise_id})
        if result.deleted_count == 1:
            return SuccessModel()
        #
        raise HTTPException(status_code=404, detail="Franchise not found.")
