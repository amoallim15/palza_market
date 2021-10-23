from fastapi import Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from src.core.utils import update_image, short_uuid
from src.core.model import ListModel, SuccessModel
from src.core.enums import UserRole

from src.models.notice import (
    NoticeModel,
    CreateNoticeModel,
    UpdateNoticeModel,
)


def main(app):
    @app.get("/notice", response_model=ListModel)
    async def notices(
        page: int = Query(0, ge=0), keywords: str = "", page_size: int = 10
    ):
        _filter = {
            "$lookup": {
                "from": "notice_categories",
                "localField": "category_id",
                "foreignField": "_id",
                "as": "category",
            }
        }
        if keywords:
            _filter.update({"$text": {"$search": keywords}})
        #
        cursor = (
            app.db["notices"]
            .find(_filter)
            .sort("_id", -1)
            .skip(page * page_size)
            .limit(page_size)
        )
        count = await app.db["notices"].count_documents({})
        data_list = []
        #
        async for notice in cursor:
            data_list.append(NoticeModel(**notice))
        #
        return ListModel(page=page, count=count, data=data_list)

    @app.get("/notice/{notice_id}", response_model=NoticeModel)
    async def get_notice(notice_id: str):
        data = await app.db["notices"].find_one({"_id": notice_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Notice not found.")
        #
        return NoticeModel(**data)

    @app.post("/notice", response_model=NoticeModel)
    async def create_notice(
        notice: CreateNoticeModel = Body(...), current_user=Depends(app.current_user)
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        notice_category = app.db["notice_categories"].find_one(
            {"_id": notice.category_id}
        )
        if not notice_category:
            raise HTTPException(
                status_code=400, detail="Notice category does not exist."
            )
        #
        notice.thumbnail_url = update_image(
            app=app,
            old_path=notice.thumbnail_url,
            new_path=f"notices/{notice.id}",
            name=f"{short_uuid()}-thumbnail",
        )
        #
        notice = jsonable_encoder(notice)
        #
        result = await app.db["notices"].insert_one(notice)
        data = await app.db["notices"].find_one({"_id": result.inserted_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Notice not found.")
        #
        return NoticeModel(**data)

    @app.put("/notice/{notice_id}", response_model=NoticeModel)
    async def update_notice(
        notice_id: str,
        notice: UpdateNoticeModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        if "tmp" in notice.thumbnail_url:
            notice.thumbnail_url = update_image(
                app=app,
                old_path=notice.thumbnail_url,
                new_path=f"notices/{notice_id}",
                name=f"{short_uuid()}-thumbnail",
            )
        #
        notice = jsonable_encoder(notice)
        #
        await app.db["notices"].update_one({"_id": notice_id}, {"$set": notice})
        data = await app.db["notices"].find_one({"_id": notice_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Notice not found.")
        #
        return NoticeModel(**data)

    @app.delete("/notice/{notice_id}", response_model=SuccessModel)
    async def delete_notice(
        notice_id: str,
        current_user=Depends(app.current_user),
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        result = await app.db["notices"].delete_one({"_id": notice_id})
        if result.deleted_count == 1:
            return SuccessModel()
        #
        raise HTTPException(status_code=404, detail="Notice not found.")
