from fastapi import Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from src.core.utils import update_image, short_uuid
from src.core.model import ListModel, SuccessModel
from src.core.enums import UserRole

from src.models.magazine import (
    MagazineModel,
    CreateMagazineModel,
    UpdateMagazineModel,
    PatchMagazineModel,
)


def main(app):
    @app.get("/magazine", response_model=ListModel)
    async def magazines(page: int = Query(0, ge=0), page_size: int = 10):
        cursor = (
            app.db["magazines"]
            .find()
            .sort("_id", -1)
            .skip(page * page_size)
            .limit(page_size)
        )
        count = await app.db["magazines"].count_documents({})
        data_list = []
        #
        async for magazine in cursor:
            data_list.append(MagazineModel(**magazine))
        #
        return ListModel(page=page, count=count, data=data_list)

    @app.get("/magazine/{magazine_id}", response_model=MagazineModel)
    async def get_magazine(magazine_id: str):
        data = await app.db["magazines"].find_one({"_id": magazine_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Magazine not found.")
        #
        return MagazineModel(**data)

    @app.post("/magazine", response_model=MagazineModel)
    async def create_magazine(
        magazine: CreateMagazineModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        magazine.thumbnail_url = update_image(
            app=app,
            old_path=magazine.thumbnail_url,
            new_path=f"magazines/{magazine.id}",
            name=f"{short_uuid()}-thumbnail",
        )
        #
        magazine = jsonable_encoder(magazine)
        #
        result = await app.db["magazines"].insert_one(magazine)
        data = await app.db["magazines"].find_one({"_id": result.inserted_id})
        #
        return MagazineModel(**data)

    @app.put("/magazine/{magazine_id}", response_model=MagazineModel)
    async def update_magazine(
        magazine_id: str,
        magazine: UpdateMagazineModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        if "tmp" in magazine.thumbnail_url:
            magazine.thumbnail_url = update_image(
                app=app,
                old_path=magazine.thumbnail_url,
                new_path=f"magazines/{magazine_id}",
                name=f"{short_uuid()}-thumbnail",
            )
        #
        magazine = jsonable_encoder(magazine)
        #
        await app.db["magazines"].update_one({"_id": magazine_id}, {"$set": magazine})
        data = await app.db["magazines"].find_one({"_id": magazine_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Magazine not found.")
        #
        return MagazineModel(**data)

    @app.patch("/magazine/{magazine_id}", response_model=MagazineModel)
    async def patch_magazine(
        magazine_id: str, magazine: PatchMagazineModel = Body(...)
    ):
        data = await app.db["magazines"].find_one({"_id": magazine_id})
        #
        view_count = data["view_count"] + 1
        #
        await app.db["magazines"].update_one(
            {"_id": magazine_id}, {"$set": {"view_count": view_count}}
        )
        data = await app.db["magazines"].find_one({"_id": magazine_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Magazine not found.")
        #
        return MagazineModel(**data)

    @app.delete("/magazine/{magazine_id}", response_model=SuccessModel)
    async def delete_magazine(magazine_id: str, current_user=Depends(app.current_user)):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        result = await app.db["magazines"].delete_one({"_id": magazine_id})
        if result.deleted_count == 1:
            return SuccessModel()
        #
        raise HTTPException(status_code=404, detail="Magazine not found.")
