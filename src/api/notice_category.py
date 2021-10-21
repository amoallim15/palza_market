from fastapi import Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from src.core.model import ListModel
from fastapi.responses import JSONResponse
from src.core.enums import UserRole

from src.models.notice import (
    NoticeCategoryModel,
    UpdateNoticeCategoryModel,
)


def main(app):
    @app.get("/notice-category")
    async def notice_categories():
        cursor = app.db["notice_categories"].find()
        data_list = []
        #
        async for notice_category in cursor:
            data_list.append(NoticeCategoryModel(**notice_category))
        #
        return ListModel(page=0, count=len(data_list), data=data_list)

    @app.get("/notice-category/{notice_category_id}")
    async def get_notice_category(notice_category_id: str):
        data = await app.db["notice_categories"].find_one({"_id": notice_category_id})
        if data is None:
            raise HTTPException(status_code=404, detail="notice category not found.")
        #
        return NoticeCategoryModel(**data)

    @app.post("/notice-category")
    async def create_notice_category(
        notice_category: NoticeCategoryModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        duplicate_notice_category = app.db["notice_categories"].find_one(
            {"label": notice_category.label}
        )
        if duplicate_notice_category:
            raise HTTPException(status_code=400, detail="Duplicated notice category.")
        #
        notice_category = jsonable_encoder(notice_category)
        result = await app.db["notice_categories"].insert_one(notice_category)
        data = await app.db["notice_categories"].find_one({"_id": result.inserted_id})
        #
        return NoticeCategoryModel(**data)

    @app.put("/notice-category/{notice_category_id}")
    async def update_notice_category(
        notice_category_id: str,
        notice_category: UpdateNoticeCategoryModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        notice_category = jsonable_encoder(notice_category)
        await app.db["notice_categories"].update_one(
            {"_id": notice_category_id}, {"$set": notice_category}
        )
        data = await app.db["notice_categories"].find_one({"_id": notice_category_id})
        #
        return NoticeCategoryModel(**data)

    @app.delete("/notice-category/{notice_category_id}")
    async def delete_notice_category(
        notice_category_id: str,
        current_user=Depends(app.current_user),
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        result = await app.db["notice_categories"].delete_one(
            {"_id": notice_category_id}
        )
        if result.deleted_count == 1:
            return JSONResponse(status_code=204)
        #
        raise HTTPException(status_code=404, detail="Notice Category not found.")
