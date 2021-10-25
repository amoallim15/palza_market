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
        pipeline = []
        if keywords:
            pipeline.append({"$match": {"$text": {"$search": keywords}}})
        #
        pipeline += [
            {
                "$lookup": {
                    "from": "notice_categories",
                    "localField": "category_id",
                    "foreignField": "_id",
                    "as": "category",
                }
            },
            {"$unwind": "$category"},
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
            result = await app.db["notices"].aggregate(pipeline).next()
        except StopAsyncIteration:
            result = {"info": {"count": 0, "page": page, "page_size": page_size}}
        return ListModel(**result)

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
