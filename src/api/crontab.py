from fastapi import Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from src.core.model import ListModel  # , SuccessModel
from src.core.enums import UserRole

from src.models.crontab import (
    CrontabModel,
    UpdateCrontabModel,
    CreateCrontabModel,
)


def main(app):
    @app.get("/crontab", response_model=ListModel)
    async def crontabs(
        page: int = Query(0, ge=0),
        current_user=Depends(app.current_user),
        page_size: int = 10,
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
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
            result = await app.db["crontabs"].aggregate(pipeline).next()
        except StopAsyncIteration:
            result = {"info": {"count": 0, "page": page, "page_size": page_size}}
        return ListModel(**result)

    @app.get("/crontab/{crontab_id}", response_model=CrontabModel)
    async def get_crontab(crontab_id: str, current_user=Depends(app.current_user)):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        data = await app.db["crontabs"].find_one({"_id": crontab_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Crontab not found.")
        #
        return CrontabModel(**data)

    @app.post("/crontab", response_model=CrontabModel)
    async def create_crontab(
        current_user=Depends(app.current_user), crontab: CreateCrontabModel = Body(...)
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        # TODO: run the crontab script..
        crontab = jsonable_encoder(crontab)
        #
        result = await app.db["crontabs"].insert_one(crontab)
        data = await app.db["crontabs"].find_one({"_id": result.inserted_id})
        #
        if data is None:
            raise HTTPException(status_code=404, detail="Crontab not found.")
        #
        return CrontabModel(**data)

    @app.put("/crontab/{crontab_id}", response_model=CrontabModel)
    async def update_crontab(
        crontab_id: str,
        crontab: UpdateCrontabModel = Body(...),
        current_user=Depends(app.current_user),
    ):
        if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
            raise HTTPException(status_code=403, detail="Not allowed.")
        #
        crontab = jsonable_encoder(crontab)
        #
        await app.db["crontabs"].update_one({"_id": crontab_id}, {"$set": crontab})
        data = await app.db["crontabs"].find_one({"_id": crontab_id})
        if data is None:
            raise HTTPException(status_code=404, detail="Crontab not found.")
        #
        return CrontabModel(**data)

    # @app.delete("/crontab/{crontab_id}", response_model=SuccessModel)
    # async def delete_crontab(
    #     crontab_id: str,
    #     current_user=Depends(app.current_user),
    # ):
    #     if current_user.user_role not in [UserRole.ADMIN, UserRole.EMPLOYEE]:
    #         raise HTTPException(status_code=403, detail="Not allowed.")
    #     #
    #     result = await app.db["crontabs"].delete_one({"_id": crontab_id})
    #     if result.deleted_count == 1:
    #         return SuccessModel()
    #     #
    #     raise HTTPException(status_code=404, detail="Crontab not found.")
